from flask import Flask, request, jsonify, render_template, send_file
from dotenv import load_dotenv
import os
from db_handler import db_handler
from exceptions import UserAlreadyExists, IncorrectCredentials
from assistant import Assistant
import route_handler as rh
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains



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
    return routes

@app.route("/get-map")
def get_map():
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) as driver: 
        driver.get('https://www.google.com/maps/dir/899+Nebo+Rd,+Hannon,+ON+L0R+1P0,+Canada/91+Osler+Dr,+Hamilton,+ON+L9H+4H4,+Canada/700+Main+St+W,+Hamilton,+ON+L8S+1A5,+Canada/')
        # Scroll down till the end
        driver.find_element(By.CSS_SELECTOR, ".yra0jd").click()
        specific_element = driver.find_element(By.CSS_SELECTOR, "canvas.aFsglc:nth-child(1)")
        actions = ActionChains(driver)
        actions.move_to_element(specific_element).perform()
        # Take a screenshot of just the located element and save it to a file
        driver.implicitly_wait(.6)
        specific_element.screenshot('map.png')
    
    
        # Close the browser
        driver.quit()
    return send_file("map.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)