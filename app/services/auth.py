from flask import flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.core.database import db
from app.models import User


def login(form):
    user = User.query.filter_by(username=form["username"]).first()
    if user and check_password_hash(user.password, form["password"]):
        login_user(user)
        flash("Login successful.", "success")
        return redirect(url_for("api.chatrooms"))
    flash("Invalid username or password.", "danger")
    return redirect(url_for("api.login"))


def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("api.index"))


def register(form):
    username = form["username"]
    email = form["email"]
    password = form["password"]
    user = User(username=username, email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    flash("Registration successful. You can now log in.", "success")
    return redirect(url_for("api.login"))
