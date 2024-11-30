from flask import Flask, request
import google_calendar

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    if request.is_json:
        data = request.json
        segments = data.get('segments', [])
        for segment in segments:
            text = segment.get("text", "No text available")
            print(f"Received text: {text}")  # Print the received text
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
        return 'Text processed', 200
    else:
        return 'Invalid Request', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)