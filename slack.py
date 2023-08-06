import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request

SLACK_BOT_TOKEN="xapp-1-A05M76LAYRE-5697526148050-9d7ebb3b547de2ab3bd9cbdc598a19915dcfba13ce32e54cf3c194b911ace76e"
app = Flask(__name__)
client = WebClient(token=os.environ[SLACK_BOT_TOKEN])

def handle_command(command, args):
    if command == "/greet":
        if args:
            response_text = f"Hello, {' '.join(args)}!"
        else:
            response_text = "Hello there!"
    elif command == "/weather":
        if args:
            # You would integrate with a weather API to get real weather data here
            response_text = f"The weather in {' '.join(args)} is sunny."
        else:
            response_text = "Please specify a location for weather information."
    else:
        response_text = "I'm sorry, I don't understand that command."

    return response_text

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    if 'event' in data and 'text' in data['event']:
        text = data['event']['text']
        if text.startswith('/'):
            command, *args = text.split()
            response_text = handle_command(command, args)
            
            try:
                response = client.chat_postMessage(
                    channel=data['event']['channel'],
                    text=response_text
                )
                return '', 200
            except SlackApiError as e:
                return f"Error: {e.response['error']}", 500

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
