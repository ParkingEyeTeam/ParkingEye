from dotenv import load_dotenv
import os

load_dotenv()

mongo_config = {
    'host': os.getenv('MONGO_HOST'),
    'db': 'parking_eye'
}

mongo_connection_string = f"mongodb://{mongo_config['host']}"
