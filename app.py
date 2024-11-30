from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    if request.is_json:
        data = request.json
        segments = data.get('segments', [])
        for segment in segments:
            text = segment.get("text", "No text available")
            print(f"Received text: {text}")  # Print the received text
        return 'Text processed', 200
    else:
        return 'Invalid Request', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)