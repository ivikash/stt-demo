from flask import Flask
from flask_socketio import SocketIO

from app.core.config import config
from app.core.database import db
from app.core.logger import logger
from app.core.security import login_manager
from app.core.webrtc import webrtc_manager

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Initialize database
db.init_app(app)

# Initialize Flask-SocketIO
socketio = SocketIO(app, async_mode="asgi")

# Initialize Flask-Login
login_manager.init_app(app)

# Initialize WebRTC manager
webrtc_manager.init_app(app)

# Import routes
from app.api import routes
