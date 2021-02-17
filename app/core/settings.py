SECRET_KEY = "bz47b73d9fb112e5c4b73cab4f3f3f4a2f6c8b6c7b956c383cf0dae5b426f6e9"
SECURITY_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200

# Mongo configuration
MONGO_MAX_CONNECTIONS = 500
MONGO_DB = "ocr"
MONGO_URL = f"mongodb+srv://ocr:nAHx7UZ2gj9Sda9u@cluster0-eu-west-1.zhq04.mongodb.net/{MONGO_DB}?retryWrites=true&w=majority"