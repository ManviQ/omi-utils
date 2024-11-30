from flask import Flask, request
import logging
#from openai import OpenAI
#from task_classification import categorize_command
from flask import Flask, request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle


SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/gmail.send']



#log = logging.getLogger('werkzeug')
#log.disabled = True

app = Flask(__name__)

conversation_text = ""
command_active = False
command_text = ""
MAX_WORD_COUNT = 100

def authenticate_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(r'Assets\OAuthCredentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


@app.route('/app', methods=['GET', 'POST'])
def app_webhook():
    global conversation_text, command_active, command_text

    if request.method == 'GET':
        return "App endpoint is active. Please send a POST request with JSON data.", 200

    if request.is_json:
        data = request.json
        segments = data.get('segments', [])
        for segment in segments:
            text = segment.get("text", "No text available")
            conversation_text += text + "\n"
            normalized_text = text.lower()

            if "hey omi" in normalized_text:
                command_active = True
                command_text = ""

            if command_active:
                command_text += " " + text
                word_count = len(command_text.split())

                # if "thankyou omi" in normalized_text or word_count > MAX_WORD_COUNT:
                   
                #     start_index = command_text.lower().find("hey omi")
                #     end_index = command_text.lower().find("thankyou omi") + len("thankyou omi")
                #     if end_index == -1:
                #         end_index = None
                #     final_command = command_text[start_index:end_index].strip()
                #     category = categorize_command(final_command)

                    
                #     if category == 'Jira':
                #         execute_jira(final_command)

                #     elif category == 'Google Docs':
                #         print("Google Docs")

                #     elif category == 'Mail':
                #         print("Mail")

                #     elif category == 'Google Calendar':
                #         print("Google Calendar")

                #     else:
                #         print("Command is outside the supported capabilities.")


                #     command_active = False
                #     command_text = ""

        return 'Text processed', 200
    else:
        return 'Invalid Request', 400


@app.route('/setup', methods=['GET', 'POST'])
def setup_webhook():
    authenticate_google()
    return 'Google authentication setup complete', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)