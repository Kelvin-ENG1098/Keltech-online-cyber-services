from asgiref.wsgi import WsgiToAsgi

# Import the Flask app instance from the project root
from app import app as flask_app

# Wrap the WSGI Flask app with an ASGI adapter
app = WsgiToAsgi(flask_app)
