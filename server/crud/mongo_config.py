from dotenv import load_dotenv
import os

load_dotenv()

mongo_config = {
    'host': os.getenv('MONGO_HOST'),
    'db': os.getenv('MONGO_DB')
    # 'db': 'parking_eye'
}

mongo_connection_string = f"mongodb://{mongo_config['host']}"
