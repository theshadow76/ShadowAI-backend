import requests
from env import PaymentData
from help.helper_functions import GenRandomString
import base64
import json

class PayPalAPI:
    def __init__(self):
        credentials = f"{PaymentData.PAYPAL_SANDBOX_CLIENT_ID}:{PaymentData.PAYPAL_SANDBOX_SECRET_KEY_1}"
        basic_auth = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Prefer': 'return=representation',
            'Authorization': f'Basic {basic_auth}'
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
        ID = GenRandomString(10)
        ID2 = GenRandomString(5)
        self.headers.update({'PayPal-Request-Id': f'PLAN-{ID}-{ID2}'})
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
    
    def create_subscription(self, plan_id, start_time, quantity, shipping_amount, subscriber, application_context):
        url = 'https://api-m.sandbox.paypal.com/v1/billing/subscriptions'
        ID = GenRandomString(10)
        ID2 = GenRandomString(5)
        credentials = f"{PaymentData.PAYPAL_SANDBOX_CLIENT_ID}:{PaymentData.PAYPAL_SANDBOX_SECRET_KEY_1}"
        basic_auth = base64.b64encode(credentials.encode()).decode()
        self.headers.update({
            'PayPal-Request-Id': f'SUBSCRIPTION-{ID}-{ID2}',
            'Authorization': f'Basic {basic_auth}'
        })
        data = {
            "plan_id": plan_id,
            "start_time": start_time,
            "quantity": quantity,
            "shipping_amount": shipping_amount,
            "subscriber": subscriber,
            "application_context": application_context
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
        prod_id = product_response.json()['id']
        return prod_id
    def CreatePlan(self):
        product_id = self.CreateProduct()
        plan_response = self.paypal_api.create_plan(
        product_id=product_id,
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
            {
                "frequency": {
                    "interval_unit": "MONTH",
                    "interval_count": 1
                },
                "tenure_type": "REGULAR",
                "sequence": 2,
                "total_cycles": 12,  # Or another number according to your plan
                "pricing_scheme": {
                    "fixed_price": {
                        "value": PaymentData.SUB_1_PRICE_USD,
                        "currency_code": "USD"
                    }
                }
            }
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
        return f"The plan response is: {plan_response.json()}"
    
    def CreateSubscription(self):
        plan_id = "P-5ML4271244454362WXNWU5NQ"  # Replace with actual plan_id from your CreatePlan method
        start_time = "2018-11-01T00:00:00Z"
        quantity = "20"
        shipping_amount = {
            "currency_code": "USD",
            "value": "10.00"
        }
        subscriber = {
            "name": {
                "given_name": "John",
                "surname": "Doe"
            },
            "email_address": "customer@example.com",
            "shipping_address": {
                "name": {
                    "full_name": "John Doe"
                },
                "address": {
                    "address_line_1": "2211 N First Street",
                    "address_line_2": "Building 17",
                    "admin_area_2": "San Jose",
                    "admin_area_1": "CA",
                    "postal_code": "95131",
                    "country_code": "US"
                }
            }
        }
        application_context = {
            "brand_name": "walmart",
            "locale": "en-US",
            "shipping_preference": "SET_PROVIDED_ADDRESS",
            "user_action": "SUBSCRIBE_NOW",
            "payment_method": {
                "payer_selected": "PAYPAL",
                "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
            },
            "return_url": "https://example.com/returnUrl",
            "cancel_url": "https://example.com/cancelUrl"
        }
        subscription_response = self.paypal_api.create_subscription(
            plan_id=plan_id,
            start_time=start_time,
            quantity=quantity,
            shipping_amount=shipping_amount,
            subscriber=subscriber,
            application_context=application_context
        )
        return f"The subscription response is: {subscription_response.json()}"



    def execute(self):
        pass