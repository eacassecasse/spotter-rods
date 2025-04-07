import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
environ_path = load_dotenv(os.path.join(BASE_DIR, '.env'))
load_dotenv(environ_path)

ENV = os.environ
