import os

HOST = os.environ.get("MYSQLHOST")
USER = os.environ.get("MYSQLUSER")
PASSWORD = os.environ.get("MYSQLPASSWORD")
DATABASE = os.environ.get("MYSQLDATABASE")
PORT = int(os.environ.get("MYSQLPORT", "3306"))