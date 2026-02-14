from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Incident
from . import db
import bcrypt

main = Blueprint("main", __name__)

@main.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and bcrypt.checkpw(request.form["password"].encode(), user.password_hash.encode()):
            login_user(user)
            return redirect(url_for("main.index"))
        flash("Invalid credentials","danger")
    return render_template("login.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route("/")
@login_required
def index():
    incidents = Incident.query.order_by(Incident.id.desc()).all()
    return render_template("index.html", incidents=incidents)

@main.route("/create", methods=["POST"])
@login_required
def create():
    incident = Incident(title=request.form["title"], description=request.form["description"])
    db.session.add(incident)
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route("/resolve/<int:id>")
@login_required
def resolve(id):
    incident = Incident.query.get_or_404(id)
    incident.resolve()
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route("/delete/<int:id>")
@login_required
def delete(id):
    if current_user.role != "admin":
        return "Forbidden",403
    incident = Incident.query.get_or_404(id)
    db.session.delete(incident)
    db.session.commit()
    return redirect(url_for("main.index"))
