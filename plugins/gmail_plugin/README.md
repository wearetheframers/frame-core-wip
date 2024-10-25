# Gmail Plugin Example

This example demonstrates how to use the `GmailPlugin` with the Frame framework to read the latest emails from a Gmail account.

## Setup

1. Ensure you have the necessary dependencies installed. You can install them using:

   ```bash
   pip install -r requirements.txt
   ```

2. Navigate to the `examples/gmail_plugin_example` directory.

3. Update the `config.json` file with your Gmail API key.

4. Run the main script to see the plugin in action:

   ```bash
   python main.py
   ```

## How It Works

- The `GmailPlugin` is registered with a Framer instance.
- The plugin provides an action `read_emails` that fetches the latest emails from Gmail.
- The main script calls the `read_emails` action to retrieve and display the latest email subjects.

## Customization

You can customize the plugin to handle different email operations. Modify the `read_emails` method in `gmail_plugin.py` to add more functionalities.

## License

This example is provided under the MIT License. See the LICENSE file for more details.
# Gmail Plugin Example

This example demonstrates how to use the Gmail API to read emails and list Gmail labels using a plugin architecture.

## Prerequisites

- Python 3.10.7 or greater
- The pip package management tool
- A Google Cloud project
- A Google account with Gmail enabled

## Setup

1. **Enable the Gmail API:**
   - Go to the Google Cloud console and enable the Gmail API for your project.

2. **Configure OAuth Consent Screen:**
   - Set up the OAuth consent screen in the Google Cloud console.

3. **Authorize Credentials:**
   - Create OAuth 2.0 Client IDs for a desktop application in the Google Cloud console.
   - Save the downloaded JSON file as `credentials.json` in your working directory.

4. **Install Dependencies:**
   - Run the following command to install the required libraries:
     ```bash
     pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
     ```

## Running the Example

1. **Run the Quickstart Script:**
   - Execute the `quickstart.py` script to authenticate and list Gmail labels:
     ```bash
     python quickstart.py
     ```

2. **Using the Plugin:**
   - The `GmailPlugin` class can be integrated into a larger application to read emails.

## Environment Variables

- `GMAIL_API_KEY`: The API key for accessing the Gmail API, stored in `config.json`.

## Notes

- This example uses a simplified authentication approach suitable for testing environments. For production, consider a more secure authentication method.
