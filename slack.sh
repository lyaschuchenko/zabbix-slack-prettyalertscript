#!/bin/bash

# Slack incoming web-hook URL and user name
url='CHANGEME'             # example: https://hooks.slack.com/services/QW3R7Y/D34DC0D3/BCADFGabcDEF123
username='Zabbix'

## Values received by this script:
# To = $1 (Slack channel or user to send the message to, specified in the Zabbix web interface; "@username" or "#channel")
# Subject = $2 (usually either PROBLEM or RECOVERY)
# Message = $3 (whatever message the Zabbix action sends, preferably something like "Zabbix server is unreachable for 5 minutes - Zabbix server (127.0.0.1)")

# Get the Slack channel or user ($1) and Zabbix subject ($2 - hopefully either PROBLEM or RECOVERY)
to="$1"
subject=$(echo $2|cut -d' ' -f1)
server=$(echo $2|cut -d' ' -f2-)

# Set up the alert type (future flexibility)
if [ "$subject" == 'RECOVERY' ]; then
        type="R"
elif [ "$subject" == 'PROBLEM' ]; then
        type="P"
else
        type="N"
fi


# Change message emoji depending on the subject - smile (RECOVERY), frowning (PROBLEM), or ghost (for everything else)
if [ $type == 'R' ]; then
        emoji=':smile:'
        color="#20E020"
        status="Recovered"
elif [ $type == 'P' ]; then
        emoji=':frowning:'
        color="#E02020"
        status="Problem"
else
        emoji=':ghost:'
        color="#808080"
        status="N/A"
fi

# The message that we want to send to Slack is the "subject" value ($2 / $subject - that we got earlier)
#  followed by the message that Zabbix actually sent us ($3)
message="$3"

# Build our JSON payload and send it as a POST request to the Slack incoming web-hook URL
# See https://api.slack.com/docs/formatting for formatting details
payload="payload={
        \"channel\": \"${to}\",
        \"username\": \"${username}\",
        \"icon_emoji\": \"${emoji}\",
        \"attachments\": [
           {
                \"title\": \"${server}: ${status}\",
                \"fallback\": \"${message}\",
                \"text\": \"${message}\",
                \"color\": \"${color}\",
                \"mrkdwn_in\": [ \"text\" ]
           }
        ] }"

/usr/bin/curl -m 5 --data-urlencode "${payload}" $url
