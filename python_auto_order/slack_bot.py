from flask import Flask, redirect, url_for, request
from flask import Response
import json
app = Flask(__name__)

@app.route('/slack', methods=['POST','GET'])
def slack():
    payload = request.get_data()
    data = json.loads(payload)
    return Response(data["challenge"], mimetype='application/x-www-form-urlencoded')

@app.route('/oauth', methods=['POST'])
def oauth():
    code = request.args.get('code')
    r = request.post("https://slack.com/api/oauth.access", data={'client_id':'아이디', 'client_secret':'시크릿', 'code':code, 'redirect_uri' : '선택사항'})
    response = json.loads(r.text)
    access_token = response['access_token']
    return 'auth success'

#app.run(host='0.0.0.0', port = 3030, debug='True')

import os
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token='xoxb-',
    signing_secret='2'
)
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button..버튼을 눌렀군..")

@app.action("approve_button")
def approve_request(ack, say):
    # Acknowledge action request
    ack()
    say("Request approved 👍")

@app.command("/echo")
def repeat_text(ack, say, command):
    # Acknowledge command request
    ack()
    say(f"버튼을 눌렀군...{command['text']}")

@app.message("-help")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"아직 이벤트 핸들러 안만들었어...")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3030)))
