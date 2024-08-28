from flask import Flask, request, jsonify, Response, render_template
from meta_ai_api import MetaAI

app = Flask(__name__)
ai = MetaAI()

@app.route('/')
def index():
    return render_template('index.html')

def stream_response(user_message):
    response = ai.prompt(message=user_message, stream=True)
    for r in response:
        yield f"data: {r['message']}\n\n"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'message': 'Please provide a message.'}), 400

    return Response(stream_response(user_message), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
