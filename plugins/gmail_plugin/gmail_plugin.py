import os
import json
import logging
from typing import Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
from bs4 import BeautifulSoup
import dateutil.parser as parser
import csv
from frame.src.framer.brain.plugins.base import BasePlugin

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailPlugin(BasePlugin):
    def __init__(self, framer=None, token_file_path=None):
        super().__init__(framer)
        self.logger = logging.getLogger(self.__class__.__name__)
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.token_file_path = os.path.join(curr_dir, 'token.json')
        self.credentials_file_path = os.path.join(curr_dir, 'credentials.json')
        self.api_key = None

    async def on_load(self, framer):
        self.framer = framer
        self.logger.info("GmailPlugin loaded")
        self.load_config()
        self.register_actions(framer.brain.action_registry)

    def load_config(self):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(curr_dir, "config.json")
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            self.api_key = config.get("GMAIL_API_KEY")
            self.client_id = config.get("GMAIL_CLIENT_ID", os.getenv("GMAIL_CLIENT_ID"))
            self.client_secret = config.get("GMAIL_CLIENT_SECRET", os.getenv("GMAIL_CLIENT_SECRET"))

    def register_actions(self, action_registry):
        self.add_action(
            name="read_emails",
            action_func=self.read_emails,
            description="Read the latest emails from Gmail",
        )
        self.csv_file_name = "emails.csv"

    async def read_emails(self, execution_context: Any) -> str:
        try:
            creds = self.get_credentials()
            service = build('gmail', 'v1', credentials=creds)
            unread_msgs = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=10).execute()
            mssg_list = unread_msgs.get('messages', [])

            if not mssg_list:
                return "No new emails found."

            final_list = []
            for mssg in mssg_list:
                temp_dict = {}
                m_id = mssg['id']
                message = service.users().messages().get(userId='me', id=m_id).execute()
                payld = message['payload']
                headr = payld['headers']

                for one in headr:
                    if one['name'] == 'Subject':
                        temp_dict['Subject'] = one['value']
                    elif one['name'] == 'Date':
                        msg_date = one['value']
                        date_parse = parser.parse(msg_date)
                        temp_dict['Date'] = str(date_parse.date())
                    elif one['name'] == 'From':
                        temp_dict['Sender'] = one['value']

                temp_dict['Snippet'] = message.get('snippet', '')

                try:
                    mssg_parts = payld.get('parts', [])
                    if mssg_parts:
                        part_one = mssg_parts[0]
                        part_body = part_one.get('body', {})
                        part_data = part_body.get('data', '')
                        clean_one = part_data.replace("-", "+").replace("_", "/")
                        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))
                        soup = BeautifulSoup(clean_two, "lxml")
                        temp_dict['Message_body'] = soup.body
                    else:
                        temp_dict['Message_body'] = "No message body available"
                except Exception as e:
                    self.logger.error(f"Failed to parse message body: {e}")

                final_list.append(temp_dict)
                service.users().messages().modify(userId='me', id=m_id, body={'removeLabelIds': ['UNREAD']}).execute()

            self.export_to_csv(final_list)
            for email in final_list:
                print(f"Sender: {email['Sender']}")
                print(f"Subject: {email['Subject']}")
                print(f"Date: {email['Date']}")
                print(f"Snippet: {email['Snippet']}")
                print(f"Message Body: {email['Message_body']}\n")
            
            return f"Total messages retrieved and printed: {len(final_list)}"

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return "An error occurred while trying to read emails."

    def get_credentials(self):
        creds = None
        if os.path.exists(self.token_file_path):
            creds = Credentials.from_authorized_user_file(self.token_file_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_file_path, 'w') as token:
                token.write(creds.to_json())
        return creds

    def export_to_csv(self, data):
        example_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../examples/gmail_plugin_example')
        csv_file_path = os.path.join(example_dir, self.csv_file_name)
        with open(csv_file_path, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['Sender', 'Subject', 'Date', 'Snippet', 'Message_body']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()
            for val in data:
                writer.writerow(val)

    async def on_remove(self):
        self.logger.info("GmailPlugin removed")
