from flask import Flask, request
from flask_cors import CORS

from Backend.GPTMode import OpenAIModel
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:*"}})

model = OpenAIModel()

@app.route('/image', methods=['GET'])
def root():
    prompt = request.args.get('prompt')
    user_id = request.args.get('user_id')
    chat_id = request.args.get('chat_id')
    conv = model.run_conversation(prompt=prompt, chat_id=chat_id, user_id=user_id)
    return conv

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
