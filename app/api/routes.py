from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app.api import api
from app.core import db, socketio
from app.models import User, ChatRoom, Message
from app.services import auth_service, chatroom_service, message_service


@api.route("/")
def index():
    return render_template("index.html")


@api.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle login form
        return auth_service.login(request.form)
    return render_template("login.html")


@api.route("/logout")
@login_required
def logout():
    return auth_service.logout()


@api.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Handle registration form
        return auth_service.register(request.form)
    return render_template("register.html")


@api.route("/chatrooms")
@login_required
def chatrooms():
    chatrooms = chatroom_service.get_chatrooms(current_user)
    return render_template("chatrooms.html", chatrooms=chatrooms)


@api.route("/chatrooms/<int:id>", methods=["GET", "POST"])
@login_required
def chatroom(id):
    chatroom = chatroom_service.get_chatroom(id)
    if request.method == "POST":
        # Handle new message form
        message_service.create_message(chatroom, current_user, request.form["message"])
        socketio.emit("new_message", {"message": request.form["message"]}, room=str(id))
    messages = message_service.get_messages(chatroom)
    return render_template("chatroom.html", chatroom=chatroom, messages=messages)
