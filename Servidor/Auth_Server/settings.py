"""

Python Script to load environmnt variables from .env file

"""

from dotenv import load_dotenv
import os

load_dotenv()

# JWT Config
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")