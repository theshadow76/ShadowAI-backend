import requests
import json

class MercadoPagoPreapproval:
    def __init__(self, access_token):
        self.access_token = access_token
        self.url = "https://api.mercadopago.com/preapproval"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def post_preapproval(self, payload):
        response = requests.post(self.url, headers=self.headers, json=payload)
        return response

    def check_response(self, response):
        if response.status_code == 200:
            print("Successfully posted data.")
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"Failed to post data. Status code: {response.status_code}")
            print(response.text)

if __name__ == '__main__':
    # Initialize class with your access token
    mp_preapproval = MercadoPagoPreapproval("YOUR_ACCESS_TOKEN")

    # Prepare the payload
    payload = {
        "preapproval_plan_id": "2c938084726fca480172750000000000",
        "reason": "Yoga classes",
        "external_reference": "YG-1234",
        "payer_email": "test_user@testuser.com",
        "card_token_id": "e3ed6f098462036dd2cbabe314b9de2a",
        "auto_recurring": {
            "frequency": 1,
            "frequency_type": "months",
            "start_date": "2020-06-02T13:07:14.260Z",
            "end_date": "2022-07-20T15:59:52.581Z",
            "transaction_amount": 10,
            "currency_id": "ARS"
        },
        "back_url": "https://www.mercadopago.com.ar",
        "status": "authorized"
    }

    # Post the preapproval
    response = mp_preapproval.post_preapproval(payload)

    # Check the response
    mp_preapproval.check_response(response)
