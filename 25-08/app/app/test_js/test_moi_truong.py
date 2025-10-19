from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
try:
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
    print("✅ Flask-SocketIO async_mode:", socketio.async_mode)
except Exception as e:
    print("❌ Error:", e)
