from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
from datetime import datetime, timedelta

# Define the required scope for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

app = Flask(__name__)

def authenticate_google():
    """
    Authenticate the user with Google and return the Google Calendar API service object.
    """
    creds = None
    # Check if token.pickle already exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If no valid credentials, prompt the user to authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('OAuthCredentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('calendar', 'v3', credentials=creds)

def create_event(service, event):
    """
    Create an event in the user's Google Calendar.
    """
    try:
        # Insert the event into the user's calendar
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created successfully: {event_result.get('htmlLink')}"
    except HttpError as error:
        return f"An error occurred: {error}"

@app.route('/create_event', methods=['POST'])
def create_event_api():
    """
    API endpoint to create a Google Calendar event from a POST request.
    """
    try:
        data = request.get_json()
        if 'segments' not in data:
            return jsonify({"error": "Missing 'segments' in request"}), 400
        
        service = authenticate_google()

        # Define event details dynamically from the request payload
        event = {
            'summary': data.get('summary', 'Omi Hackathon Meeting'),
            'location': data.get('location', 'Virtual'),
            'description': data.get('description', 'Discussion about progress and upcoming goals for the Omi Hackathon.'),
            'start': {
                'dateTime': (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z',
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat() + 'Z',
                'timeZone': 'UTC',
            },
            'attendees': [{'email': email} for email in data.get('attendees', ['testuser1@example.com', 'testuser2@example.com'])],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        result = create_event(service, event)
        return jsonify({"message": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
