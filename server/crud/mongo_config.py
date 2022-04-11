mongo_config = {
    'host': 'localhost',
    'port': 27017,
    'db': 'parking_eye'
}

mongo_connection_string = f"mongodb://{mongo_config['host']}:{mongo_config['port']}"
