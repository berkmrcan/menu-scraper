from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into environment

API_KEY = os.getenv("API_KEY")
DEBUG = os.getenv("DEBUG")
