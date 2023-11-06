import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
from env import FIREBASE_CERTIFICATE_KEY
from firebase_admin import db

class FirePay:
    def __init__(self):
        self.ref = db.reference('users')

    def add_values(self, user_id, PaymentSubID, SubType, PaymentStatus):
        user_ref = self.ref.child(user_id)
        try:
            user_ref.set({
                'PaymentSubID': PaymentSubID,
                'SubType': SubType,
                'PaymentStatus': PaymentStatus
            })
            return {"Success": "User added to database"}
        except Exception as e:
            return {"Error": e}
    def update_status(self, user_id, new_status):
        user_ref = self.ref.child(user_id)
        user_ref.update({
            'PaymentStatus': new_status
        })

def get_firebase_database(key: str = None):
    """
    Args: 
        Optional key: Certificate of the database to use if not provided, defaults to defined
        'FIREBASE_CERTIFICATE_KEY'
    Returns a firestore.client() instance
    """
    # Initialize Firebase app
    if key:
        cred = credentials.Certificate(key)  # Replace with your Firebase project's certificate path
    else: 
        cred = credentials.Certificate(FIREBASE_CERTIFICATE_KEY)
    firebase_admin.initialize_app(cred)
    return firestore.client()
