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
