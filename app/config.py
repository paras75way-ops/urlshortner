from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")