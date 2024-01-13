from flask import Flask, request
from dotenv import load_dotenv
import os
import db_handler
from exceptions import UserAlreadyExists


load_dotenv()

dh = db_handler.db_handler()


app = Flask(__name__)

# Register Errors
@app.errorhandler(UserAlreadyExists)
def handle_invalid_usage(error):
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

    dh.register(email, password, address)

    return f"{email,name,password,address=}"

@app.route("/admin/register")
def admin_register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    address = request.form.get("address")

    dh.register(email, password, address)

    return "Registered?"


if __name__ == "__main__":
    app.run(debug=True)