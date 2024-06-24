from flask_login import current_user

from app.core.database import db
from app.models import ChatRoom


def get_chatrooms(user):
    return user.chatrooms


def get_chatroom(id):
    return ChatRoom.query.get(id)


def create_chatroom(name):
    chatroom = ChatRoom(name=name)
    db.session.add(chatroom)
    db.session.commit()
    chatroom.users.append(current_user)
    db.session.commit()
    return chatroom
