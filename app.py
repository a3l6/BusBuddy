from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv
import os
from db_handler import db_handler, IncorrectCredentials, UserAlreadyExists
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

        try:
            registerSuccess = dh.register(name, email, password, address, school)
        except UserAlreadyExists:
            registerSuccess = False

        try:
            checkAdminAcc = dh.admin_login(email, password)
        except IncorrectCredentials:
            checkAdminAcc = False

        # After registering, return to login page if successful or return to register if user already exists
        if registerSuccess and (not checkAdminAcc):
            return render_template("login.html")
        
        # WIP: implement boolean var pass/flash error message
        return render_template("register_student.html")

@app.route("/admin/register", methods=["GET", "POST"])
def admin_register():
    if request.method == "GET":
        return render_template("register_admin.html")
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        school = request.form.get("school")

        try:
            registerSuccess = dh.admin_register(name, email, password, school)
        except UserAlreadyExists:
            registerSuccess = False

        try:
            checkStudentAcc = dh.login(email, password)
        except IncorrectCredentials:
            checkStudentAcc = False

        # After registering, return to login page if successful or return to register if user already exists
        if registerSuccess and (not checkStudentAcc):
            return render_template("login.html")
        
        # WIP: implement boolean var pass/flash error message
        return render_template("register_admin.html")

# Combine login and admin login into one
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # When logging in, check if admin or student; only at most one bool here can be true
        try:
            verifiedAdmin = dh.admin_login(email, password)
        except IncorrectCredentials:
            verifiedAdmin = False

        try:
            verifiedStudent = dh.login(email, password)
        except IncorrectCredentials:
            verifiedStudent = False

        # Logged in as admin; return admin map page
        if verifiedAdmin and (not verifiedStudent):
            print("Test 1")
            return render_template("map_admin.html") 
        
        # Logged in as student; return student map page
        if (not verifiedAdmin) and verifiedStudent:
            print("Test 2")
            return render_template("map_student.html")
        
        # WIP: Redirect to login page, implement boolean var pass/flash error message
        return render_template("login.html")

@app.route("/admin/map_routes")
def admin_maps():
    return render_template("map_admin.html")

@app.route("/map_routes")
def student_maps():
    return render_template("map_student.html")

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