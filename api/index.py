import sys
import os

# Add the parent directory to Python path so we can import from root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your Flask app from app.py in the root directory
from app import app

