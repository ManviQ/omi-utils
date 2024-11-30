from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
from datetime import datetime, timedelta

# Define the required scope for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

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
            flow = InstalledAppFlow.from_client_secrets_file(r'OAuthCredentials.json', SCOPES)
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
        print(f"Event created successfully: {event_result.get('htmlLink')}")
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == '__main__':
    # Authenticate and build the Google Calendar service object
    service = authenticate_google()

    # Define event details dynamically in the main function
    event = {
        'summary': 'Omi Hackathon Meeting',  # Event title
        'location': 'Virtual',  # Location (can be physical or virtual)
        'description': 'Discussion about progress and upcoming goals for the Omi Hackathon.',  # Event description
        'start': {
            'dateTime': (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z',  # Start time: 1 day from now
            'timeZone': 'UTC',  # Timezone
        },
        'end': {
            'dateTime': (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat() + 'Z',  # End time: 1 hour later
            'timeZone': 'UTC',  # Timezone
        },
        'attendees': [
            {'email': 'testuser1@example.com'},  # Add attendees
            {'email': 'testuser2@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # Reminder 1 day before
                {'method': 'popup', 'minutes': 10},  # Reminder 10 minutes before
            ],
        },
    }

    # Create a new event in the Google Calendar
    create_event(service, event)
