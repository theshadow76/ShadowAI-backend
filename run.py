from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from GPTModel import OpenAIModel
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

model = OpenAIModel()

@app.route('/webhook-mp', methods=['POST'])
def mercado_pago_webhook():
    # Verify the request is a POST request
    if request.method != 'POST':
        abort(400)

    # Get the JSON data from the request
    data = request.get_json()

    # If data is None, that means the request did not contain valid JSON
    if data is None:
        abort(400)

    # At this point, `data` is a dictionary containing the data sent by Mercado Pago.
    # You would add your processing logic here.
    print(data)  # For debugging purposes, print the data to the console.

    # Respond to Mercado Pago to acknowledge receipt of the webhook.
    # According to the Mercado Pago documentation, you should respond with a
    # status code of 200 or 201.
    return jsonify({'status': 'success'}), 200

@app.route('/image', methods=['GET'])
def root():
    prompt = request.args.get('prompt')
    user_id = request.args.get('user_id')
    chat_id = request.args.get('chat_id')
    conv = model.run_conversation(prompt=prompt, chat_id=chat_id, user_id=user_id)
    return conv

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
