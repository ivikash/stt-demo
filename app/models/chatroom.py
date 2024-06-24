from app.core.database import db

user_chatrooms = db.Table(
    "user_chatrooms",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("chatroom_id", db.Integer, db.ForeignKey("chatrooms.id"), primary_key=True),
)


class ChatRoom(db.Model):
    __tablename__ = "chatrooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    messages = db.relationship("Message", backref="chatroom", lazy="dynamic")

    def __repr__(self):
        return f"<ChatRoom {self.name}>"
