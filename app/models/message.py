from datetime import datetime
from app.core.database import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    chatroom_id = db.Column(db.Integer, db.ForeignKey("chatrooms.id"), nullable=False)

    def __repr__(self):
        return f"<Message {self.content[:20]}...>"
