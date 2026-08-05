import os

HOST = os.environ.get("MY_SQLhost")
USER = os.environ.get("user")
PASSWORD = os.environ.get("password")
DATABASE = os.environ.get("database")
PORT = int(os.environ.get("MY_SQLPORT"))