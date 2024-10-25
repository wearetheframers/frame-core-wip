import os
import json
import base64
import logging
from typing import Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from frame.src.framer.brain.plugins.base import BasePlugin

class GmailPlugin(BasePlugin):
    def __init__(self, framer=None):
        super().__init__(framer)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api_key = None

    async def on_load(self, framer):
        self.framer = framer
        self.logger.info("GmailPlugin loaded")
        self.load_config()
        self.register_actions(framer.brain.action_registry)

    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            self.api_key = config.get("GMAIL_API_KEY")

    def register_actions(self, action_registry):
        self.add_action(
            name="read_emails",
            action_func=self.read_emails,
            description="Read the latest emails from Gmail",
        )

    async def read_emails(self, execution_context: Any) -> str:
        if not self.api_key:
            return "API key not found. Please check the config.json file."

        creds = Credentials(self.api_key)
        service = build('gmail', 'v1', credentials=creds)

        try:
            results = service.users().messages().list(userId='me', maxResults=5).execute()
            messages = results.get('messages', [])

            if not messages:
                return "No new emails found."
            
            email_summaries = []
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                email_data = msg['payload']['headers']
                subject = next(header['value'] for header in email_data if header['name'] == 'Subject')
                email_summaries.append(subject)

            return "Latest emails:\n" + "\n".join(email_summaries)

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return "An error occurred while trying to read emails."

    async def on_remove(self):
        self.logger.info("GmailPlugin removed")
