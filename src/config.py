import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SECRET_KEY = os.getenv("SECRET_KEY")


EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")


SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")

