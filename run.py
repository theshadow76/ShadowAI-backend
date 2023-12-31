from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from payments.mercadopago import ExecutePayment
from GPTModel import OpenAIModel
from payments.paypal import ExecutePayPalOrder
from Firebase import FirePay
import json

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
    print(f"The data is: {data}")  # For debugging purposes, print the data to the console.

    event_type = data.get('type')
    event_data = data.get('data')

    if event_type == 'payment':
        payment_status = event_data.get('status')
        if payment_status == 'approved':
            print('Payment was successful')
        elif payment_status == 'cancelled':
            print('Payment was canceled')
    elif event_type == 'preapproval':
        subscription_status = event_data.get('status')
    if event_type == 'subscription_preapproval':
        # Handle creation/update of subscription
        print("Subscription preapproval")
    elif event_type == 'subscription_preapproval_plan':
        # Handle creation/update of subscription plan
        print("Subscription preapproval plan")
    elif event_type == 'subscription_authorized_payment':
        # Handle creation/update of recurring payment for a subscription
        print("Subscription authorized payment")

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

@app.route('/pay', methods=['GET'])
def pay():
    sub_type = request.args.get('sub_type')
    execute_payment = ExecutePayment(sub_type=sub_type)
    response = execute_payment.pay()
    return response

@app.route('/paypal', methods=['GET'])
def paypal():
    try:
        user_id = request.args.get('user_id')
        sub_type = request.args.get('sub_type')
        execute = ExecutePayPalOrder()
        fp = FirePay()
        response1 = execute.CreateSubscription()
        
        sub_id = response1['id']
        sub_status = response1['status']

        if user_id and sub_type is not None:
            fpres = fp.add_values(user_id, sub_id, sub_type, sub_status)
            resdata = {
                "user_id": user_id,
                "sub_id": sub_id,
                "sub_type": sub_type,
                "sub_status": sub_status
            }
            with open(f'{sub_id}.json', 'w') as f:
                json.dump(resdata, f)
            return {"Success": "User added to database", "PayPalResponse": response1, "FirebaseResponse": fpres, "PayLink" : response1['links'][0]['href']}
        else:
            return {"Error": "User ID or Subscription Type is missing"}
    except Exception as e:
        return {"Error": str(e)}

@app.route('/paypal-webhook-test', methods=['POST'])
def paypal_webhook():
    # Get the webhook data sent from PayPal
    data = request.json

    # TODO: Validate and process the webhook data here
    # This is where you would typically verify the webhook data with PayPal,
    # and then process it according to your application's needs.

    if data is None:
        # No data sent in the request body
        return jsonify({"status": "invalid request"}), 400
    if data['event_type'] == 'PAYMENT.SALE.COMPLETED':
        # Payment completed successfully, take action based on the payment amount
        fp = FirePay()
        print(f"The data is: {data}")
        with open(f'{data["resource"]["billing_agreement_id"]}.json', 'r') as f:
            data = json.load(f)
        fp.update_status(data['user_id'], 'Active')
        print("Payment completed successfully")

    # For now, we'll just print the data and return a success response
    print("Received PayPal webhook:", data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) #NOTE: Change to 5000 when deploying to production
