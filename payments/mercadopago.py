import requests
import json
from env import PaymentData
from help.helper_functions import GenRandomString, get_start_end_dates

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

class ExecutePayment:
    def __init__(self, sub_type):
        self.sub_type = sub_type
        self.start_date, self.end_date = get_start_end_dates()
    def pay(self):
        # Initialize class with your access token
        mp_preapproval = MercadoPagoPreapproval(PaymentData.MERCADO_PAGO_SECRET_KEY_TEST)

        payload = {}

        if self.sub_type == "sub_1":
            # Prepare the payload
            payload = {
                "reason": PaymentData.SUB_NAME_1,
                "external_reference": PaymentData.SUB_NAME_1_id,
                "payer_email": "test_user@testuser.com",
                "auto_recurring": {
                    "frequency": 1,
                    "frequency_type": "months",
                    "start_date": self.start_date,
                    "end_date": self.end_date,
                    "transaction_amount": PaymentData.SUB_1_PRICE,
                    "currency_id": "USD"
                },
                "back_url": PaymentData.BACK_URL,
                "status": "authorized"
            }
        elif self.sub_type == "sub_2":
            payload = {
                "reason": PaymentData.SUB_NAME_2,
                "external_reference": PaymentData.SUB_NAME_2_id,
                "payer_email": "test_user@testuser.com",
                "auto_recurring": {
                    "frequency": 1,
                    "frequency_type": "months",
                    "start_date": self.start_date,
                    "end_date": self.end_date,
                    "transaction_amount": PaymentData.SUB_2_PRICE,
                    "currency_id": "USD"
                },
                "back_url": PaymentData.BACK_URL,
                "status": "authorized"
            }

        # Post the preapproval
        response = mp_preapproval.post_preapproval(payload)

        # Check the response
        mp_preapproval.check_response(response)

        return response.json()