from flask_login import UserMixin
from app.core.database import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    chatrooms = db.relationship("ChatRoom", secondary="user_chatrooms", backref="users")
    messages = db.relationship("Message", backref="author", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"