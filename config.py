import os

HOST = os.environ.get("MY_SQLhost")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
DATABASE = os.environ.get("DATABASE")
PORT = int(os.environ.get("MY_SQLport"))