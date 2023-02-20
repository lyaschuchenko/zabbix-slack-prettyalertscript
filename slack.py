#!/usr/bin/env python
import argparse
import json
import requests

# Slack incoming web-hook URL and user name
url = 'CHANGEME'             # example: https://hooks.slack.com/services/QW3R7Y/D34DC0D3/BCADFGabcDEF123
username = 'Zabbix'

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("to", help="Slack channel or user to send the message to")
parser.add_argument("subject", help="Zabbix subject, usually either PROBLEM {HOST.NAME} or RECOVERY {HOST.NAME}")
parser.add_argument("message", help="Message sent by Zabbix action, e.g. 'Zabbix server is unreachable for 5 minutes - Zabbix server (127.0.0.1)'")
args = parser.parse_args()

# Get the Slack channel or user, Zabbix subject (hopefully either PROBLEM or RECOVERY), and the server in question
to = args.to
subject = args.subject.split(' ')[0]  # The alert type is before the space, server after, e.g. "Subject: PROBLEM SomeDatabaseServer01"
server = ' '.join(args.subject.split(' ')[1:])

# Set up the alert type (future flexibility)
if subject == 'RECOVERY':
    type = 'R'
elif subject == 'PROBLEM':
    type = 'P'
else:
    type = 'N'

# Change message emoji, color, and (friendly) status depending on the subject
if type == 'R':
    emoji = ':smile:'    # A smile,
    color = "#20E020"    # and red text
    status = "Recovered"
elif type == 'P':
    emoji = ':frowning:'
    color = "#E02020"
    status = "Problem"
else:
    emoji = ':ghost:'
    color = "#808080"
    status = "N/A"

# The message that we want to send to Slack is the "subject" value (args.subject) that we got earlier,
# followed by the message that Zabbix actually sent us (args.message)
message = f"{args.subject} {args.message}"

# Build our JSON payload
payload = {
    "channel": to,
    "username": username,
    "icon_emoji": emoji,
    "attachments": [
        {
            "title": f"{server}: {status}",
            "fallback": message,
            "text": message,
            "color": color,
            "mrkdwn_in": ["text"]
        }
    ]
}

# Send the payload as a POST request to the Slack incoming web-hook URL
headers = {'Content-type': 'application/json'}
response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=5)
response.raise_for_status()
