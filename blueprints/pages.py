from flask import Blueprint, render_template, redirect, url_for, request, flash

pages = Blueprint("pages", __name__)

@pages.route("/")
def index():
    return render_template("index.html")

@pages.route("/login")
def login():
    return render_template("login.html")

@pages.route("/register-admin")
def registerAdmin():
    return render_template("register_admin.html")

@pages.route("/register-student")
def registerStudent():
    return render_template("register_student.html")




