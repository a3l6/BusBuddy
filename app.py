from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from db_handler import db_handler
from exceptions import UserAlreadyExists, IncorrectCredentials

# Blueprint imports
from blueprints.pages import pages as pages_blueprint

load_dotenv()

dh = db_handler()


app = Flask(__name__)

app.register_blueprint(pages_blueprint)

# Register Errors
@app.errorhandler(UserAlreadyExists)
def handle_user_exists(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(IncorrectCredentials)
def handle_incorrect_credentials(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



@app.route("/")
def home():
    return os.getenv("PASSWORD")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    address = request.form.get("address")
    school = request.form.get("school")

    dh.register(name, email, password, address, school)

    return f"{email,name,password,address,school=}"

@app.route("/admin/register", methods=["POST"])
def admin_register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    school = request.form.get("school")

    dh.admin_register(name, email, password, school)
    return "Registered?"

@app.route("/admin/login", methods=["POST"])
def admin_login():
    email = request.form.get("email")
    password = request.form.get("password")


    verified = dh.admin_login(email, password)

    return verified


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")


    verified = dh.login(email, password)

    return verified


if __name__ == "__main__":
    app.run(debug=True)