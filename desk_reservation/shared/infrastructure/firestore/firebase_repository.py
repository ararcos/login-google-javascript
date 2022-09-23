import firebase_admin
from decouple import config
from firebase_admin import firestore, initialize_app, credentials


class FirebaseRepository:

    data_base: firestore
    _instance = None

    def __init__(self):
        if not firebase_admin._apps:
            firebase_config = {
                "type": config("type"),
                "project_id": config("project_id"),
                "private_key_id": config("private_key_id"),
                "private_key": config("private_key").replace('\\n', '\n'),
                "client_email": config("client_email"),
                "client_id": config("client_id"),
                "auth_uri": config("auth_uri"),
                "token_uri": config("token_uri"),
                "auth_provider_x509_cert_url": config("auth_provider_x509_cert_url"),
                "client_x509_cert_url": config("client_x509_cert_url"),
            }
            cred = credentials.Certificate(firebase_config)
            initialize_app(credential=cred)
            self.data_base = firestore.client()

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance
