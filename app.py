from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from db_handler import db_handler
from exceptions import UserAlreadyExists, IncorrectCredentials
from assistant import Assistant
import route_handler as rh

# Blueprint imports
#from blueprints.pages import pages as pages_blueprint

load_dotenv()

dh = db_handler()
assistant = Assistant()

app = Flask(__name__)

#app.register_blueprint(pages_blueprint)

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
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register_student.html")
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        address = request.form.get("address")
        school = request.form.get("school")

        dh.register(name, email, password, address, school)

        return f"{email,name,password,address,school=}"

@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():
    if request.method == "GET":
        return render_template("register_admin.html")
    else:
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

# Combine login and admin login into one
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")


        verified = dh.login(email, password)

        return verified

@app.route("/get_route/<school>")
def get_route(school: str):
    return school


@app.route("/ask-ai/", methods=["GET"])
def ask():
    message = request.args["msg"]


    return assistant.query(message)


@app.route("/get-route-links")
def get_route_links():

    routes = rh.get_routes()

    urls = []

    for l in routes:
        url = "https://www.google.com/maps/dir/"
        for address in l:
            temp = address.replace(" ", "+") + "/"
            url += temp
        urls.append(url)

    #[[(long, lat), (long, lat)], [(long, lat)]]
    return urls


if __name__ == "__main__":
    app.run(debug=True)