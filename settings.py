from decouple import config

BASE_DIR = config("BASE_DIR")

AWS_ACCESS_KEY=config("AWS_ACCESS_KEY")
AWS_SECRET_KEY=config("AWS_SECRET_KEY")
AWS_REGION=config("AWS_REGION")
AWS_BUCKET_NAME=config("AWS_BUCKET_NAME")
AWS_URL=config("AWS_URL")