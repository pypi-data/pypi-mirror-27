## Mailscanner

Mailscanner is a Python 3+ library to assist in composing an email
newsletter from multiple relatively standard email messages.


### Install

Easiest done via pip `pip install pymailscanner`

### Usage

To use this module, you need to rename the `.env-example` directory to
`.env` and fill out your credentials. The ImapReader object then uses
these to log in to your email account using the standard imaplib
library.

### Examples

A minimal working example to authenticate and fetch some messages would
be like this:

``` python
import configparser
from mailscanner import *

def main():

    # Initialize configparser
    config = configparser.ConfigParser()

    # Read the credentials
    config.read('/path/to/.env/conf.ini')

    # Create a reader object
    reader = ImapReader(config)

    # Authenticate
    connection = reader.open_connection()

    # Fetch all messages in INBOX
    messages = reader.fetch_all_messages(
        connection,
        'INBOX',
        True)

    # Prints out tuples: (subject_data, message_body)
    print(messages)


if __name__ == '__main__':
    main()
```
