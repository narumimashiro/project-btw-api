import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# for local
from dotenv import load_dotenv

# if not firebase_admin._apps:
#     env = os.environ.get('ENV', 'development')
#     if env == "development":
#         load_dotenv('.env.local')
#     fb_config_json = os.getenv('FB_CONFIG_JSON')
#     fb_config_json_dict = json.loads(fb_config_json)
#     cred = credentials.Certificate(fb_config_json_dict)
#     firebase_admin.initialize_app(cred)

# db = firestore.client()

def get_firebase_client():
    if not firebase_admin._apps:  # 既に初期化されているか確認
        env = os.environ.get('ENV', 'development')
        if env == "development":
            load_dotenv('.env.local')
        fb_config_json = os.getenv('FB_CONFIG_JSON')
        fb_config_json_dict = json.loads(fb_config_json)
        cred = credentials.Certificate(fb_config_json_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()