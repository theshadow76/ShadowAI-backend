import requests
from env import PaymentData

class PayPalAPI:
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Prefer': 'return=representation'
        }

    def create_product(self, name, description, product_type, category, image_url, home_url):
        url = 'https://api-m.sandbox.paypal.com/v1/catalogs/products'
        data = {
            "name": name,
            "description": description,
            "type": product_type,
            "category": category,
            "image_url": image_url,
            "home_url": home_url
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response

    def create_plan(self, product_id, name, description, status, billing_cycles, payment_preferences, taxes):
        url = 'https://api-m.sandbox.paypal.com/v1/billing/plans'
        self.headers.update({'PayPal-Request-Id': 'PLAN-18062019-001'})
        data = {
            "product_id": product_id,
            "name": name,
            "description": description,
            "status": status,
            "billing_cycles": billing_cycles,
            "payment_preferences": payment_preferences,
            "taxes": taxes
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response


class ExecutePayPalOrder:
    def __init__(self) -> None:
        self.paypal_api = PayPalAPI()
    def CreateProduct(self):
        product_response = self.paypal_api.create_product(
            name=PaymentData.SUB_NAME_1,
            description=PaymentData.SUB_NAME_1_DESC,
            product_type="SERVICE",
            category="SOFTWARE",
            image_url=PaymentData.SUB_IMG,
            home_url=PaymentData.BACK_URL
        )
        print(product_response.text) #TODO: Get the data for the porduct ID
    def CreatePlan(self):
        plan_response = self.paypal_api.create_plan(
        product_id="PROD-XXCD1234QWER65782", #TODO: Replace with the product ID
        name=PaymentData.SUB_NAME_1,
        description=PaymentData.SUB_NAME_1_DESC,
        status="ACTIVE",
        billing_cycles=[
            {
                "frequency": {
                    "interval_unit": "MONTH",
                    "interval_count": 1
                },
                "tenure_type": "TRIAL",
                "sequence": 1,
                "total_cycles": 2,
                "pricing_scheme": {
                    "fixed_price": {
                        "value": PaymentData.SUB_1_PRICE_USD,
                        "currency_code": "USD"
                    }
                }
            },
            # ... (other billing cycles)
        ],
        payment_preferences={
            "auto_bill_outstanding": True,
            "setup_fee": {
                "value": PaymentData.SUB_1_PRICE_USD,
                "currency_code": "USD"
            },
            "setup_fee_failure_action": "CONTINUE",
            "payment_failure_threshold": 3
        },
        taxes={
            "percentage": "10",
            "inclusive": False
        }
    )
    def execute(self):
        pass