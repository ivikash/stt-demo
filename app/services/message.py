from app.core.database import db
from app.models import Message


def get_messages(chatroom):
    return chatroom.messages.order_by(Message.timestamp.desc()).all()


def create_message(chatroom, user, content):
    message = Message(content=content, author=user, chatroom=chatroom)
    db.session.add(message)
    db.session.commit()
    return message
