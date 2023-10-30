import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
from env import FIREBASE_CERTIFICATE_KEY

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
