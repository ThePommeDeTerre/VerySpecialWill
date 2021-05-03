"""

Python Script to load environmnt variables from .env file

"""

from dotenv import load_dotenv
import os

load_dotenv()

#MySQL Config
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DATABASE")

# JWT Config
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")