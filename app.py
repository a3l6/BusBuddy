from flask import Flask, request, jsonify, render_template, send_file, session, redirect, url_for
from dotenv import load_dotenv
import os
from db_handler import db_handler, IncorrectCredentials, UserAlreadyExists
from exceptions import UserAlreadyExists, IncorrectCredentials
from assistant import Assistant
import route_handler as rh
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import Digraphs
from geopy.geocoders import GoogleV3
import python_weather
import asyncio
import faker


# Blueprint imports
#from blueprints.pages import pages as pages_blueprint

load_dotenv()

dh = db_handler()
assistant = Assistant()

generated_routes = False
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

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
            return redirect(url_for("login"))
        
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
            return redirect(url_for("login"))
        
        # WIP: implement boolean var pass/flash error message
        session["name"] = name
        session["email"] = email
        session["school"] = school
        session["type"] = "admin"
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
            print(email)
            session["name"] = dh.get_admin_name(email)
            session["email"] = email
            session["school"] = dh.get_admin_school(email)
            session["type"] = "admin"
            return redirect(url_for("admin_maps"))
        
        # Logged in as student; return student map page
        if (not verifiedAdmin) and verifiedStudent:
            print("Test 2")
            session["name"] = dh.get_name(email)
            session["email"] = email
            session["school"] = dh.get_school(email)
            session["address"] = dh.get_address(email)
            session["type"] = "student"
            return redirect(url_for("student_maps"))
        
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
    return routes



@app.route("/on-load/<address>")
def get_map(address):
    loc = GoogleV3(api_key=os.getenv("GOOGLE_MAPS_KEY"))

    route = Digraphs.adress_to_route(address)
    lists = []

    def reverse(x):
        #print(x)
        return loc.reverse(f"{x[0]}, {x[1]}")
    for i in route:
        #print(f"{i[0]}, {i[1]}")
        lists.append(loc.reverse(f"{i[0]}, {i[1]}").address.replace(" ", "+"))
        #lists.append(list(map(lambda y: y.address.replace(" ", "+"),list(reverse(i)))))

    #print(lists)

    url = "https://www.google.com/maps/dir/"
    for addr in lists:
        url += addr + "/"

    idx = routes.index(url)

    # get weather
    async def getweather():
        # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            # fetch a weather forecast from a city
            weather = await client.get('Hamilton')
            
            # returns the current day's forecast temperature (int)
            return weather.current.description, weather.current.temperature

    weather = asyncio.run(getweather())



    return {"filename": f"route{idx + 1}.png", "weather": f"{weather[0]} | {weather[1]}°"}

@app.route("/generate-fake-data")
def generate_fake_data():
    addresses = [
    "93, Brian, Boulevard, Brian Boulevard, Flamborough, City of Hamilton, Ontario, Canada, L8B 0C8",
    "248, Pinehill, Drive, Pinehill Drive, Glanbrook, City of Hamilton, Ontario, Canada, L0R 1P0",
    "117, Marion, Street, Marion Street, Glanbrook, City of Hamilton, Ontario, Canada, L0R 1W0",
    "30, Fair, Street, Fair Street, Ancaster, City of Hamilton, Ontario, Canada, L9K 0A6",
    "33, Seabrooke, Drive, Seabrooke Drive, Hamilton, City of Hamilton, Ontario, Canada, L8E 1N3",
    "181, Briar Hill, Crescent, Briar Hill Crescent, Ancaster, City of Hamilton, Ontario, Canada, L9G 3P5",
    "38, Glenvale, Drive, Glenvale Drive, Hamilton, City of Hamilton, Ontario, Canada, L9C 2X6",
    "12, Ackland, Street, Ackland Street, Stoney Creek, City of Hamilton, Ontario, Canada, L8J 1H7",
    "350, East 18th, Street, East 18th Street, Hamilton, City of Hamilton, Ontario, Canada, L9A 4P9",
    "129, Glen Castle, Drive, Glen Castle Drive, Hamilton, City of Hamilton, Ontario, Canada, L8K 5Z7",
    "5, Cortina, Crescent, Cortina Crescent, Hamilton, City of Hamilton, Ontario, Canada, L8K 4K3",
    "49, Upper Walker, Avenue, Upper Walker Avenue, Stoney Creek, City of Hamilton, Ontario, Canada, L8G 1S9",
    "5, Brae Crest, Drive, Brae Crest Drive, Stoney Creek, City of Hamilton, Ontario, Canada, L8G 3A5",
    "77, 601, Governor's, Road, Governor's Road, Dundas, City of Hamilton, Ontario, Canada, L9H 7N8",
    "26, Galaxy, Boulevard, Galaxy Boulevard, Flamborough, City of Hamilton, Ontario, Canada, L8B 0Z7",
    "376, Avondale, Street, Avondale Street, Hamilton, City of Hamilton, Ontario, Canada, L8L 7C6",
    "566, 52, Southridge, Drive, Southridge Drive, Hamilton, City of Hamilton, Ontario, Canada, L9C 7W5",
    "22, West Park, Avenue, West Park Avenue, Hamilton, City of Hamilton, Ontario, Canada, L8S 3M3",
    "63, Kendrick, Court, Kendrick Court, Ancaster, City of Hamilton, Ontario, Canada, L9G 5A5",
    "254, Jacqueline, Boulevard, Jacqueline Boulevard, Hamilton, City of Hamilton, Ontario, Canada, L9B 2V7",
    "23, Grande, Avenue, Grande Avenue, Stoney Creek, City of Hamilton, Ontario, Canada, L8G 2C9",
    "12, Cresthaven, Drive, Cresthaven Drive, Stoney Creek, City of Hamilton, Ontario, Canada, L8E 4S4",
    "23, Newton, Avenue, Newton Avenue, Hamilton, City of Hamilton, Ontario, Canada, L8S 1V6",
    "43, Camp, Drive, Camp Drive, Ancaster, City of Hamilton, Ontario, Canada, L9K 0A5",
    "82, Meadow Wood, Crescent, Meadow Wood Crescent, Stoney Creek, City of Hamilton, Ontario, Canada, L8J 3Z8",
    "53, Candlewood, Court, Candlewood Court, Stoney Creek, City of Hamilton, Ontario, Canada, L8J 0C4",
    "42, Fairview, Avenue, Fairview Avenue, Hamilton, City of Hamilton, Ontario, Canada, L8L 7B4",
    "552, Main, Street, East, Main Street East, Hamilton, City of Hamilton, Ontario, Canada, L8M 1J1",
    "105, Chamomile, Drive, Chamomile Drive, Hamilton, City of Hamilton, Ontario, Canada, L8W 0B9",
    "67, Hawkswood, Trail, Hawkswood Trail, Hamilton, City of Hamilton, Ontario, Canada, L9B 2R4",
    "250, San Francisco, Avenue, San Francisco Avenue, Hamilton, City of Hamilton, Ontario, Canada, L9C 5N9",
    "87, Folkestone, Avenue, Folkestone Avenue, Hamilton, City of Hamilton, Ontario, Canada, L8V 4N1",
    "175, Rosslyn, Avenue, South, Rosslyn Avenue South, Hamilton, City of Hamilton, Ontario, Canada, L8M 3J4",
    "157, Fairfield, Avenue, Fairfield Avenue, Hamilton, City of Hamilton, Ontario, Canada, L8H 5H3",
    "44, James, Avenue, James Avenue, Stoney Creek, City of Hamilton, Ontario, Canada, L8G 3K4",
    "2058, Barton, Street, East, Barton Street East, Hamilton, City of Hamilton, Ontario, Canada, L8H 2Z4",
    "2, King, Street, East, King Street East, Dundas, City of Hamilton, Ontario, Canada, L9H 1B8",
    "380, Highland, Road, West, Highland Road West, Stoney Creek, City of Hamilton, Ontario, Canada, L8J 3W3",
    "345, Jacqueline, Boulevard, Jacqueline Boulevard, Hamilton, City of Hamilton, Ontario, Canada, L9B 2W6",
    "215, Glencairn, Avenue, Glencairn Avenue, Hamilton, City of Hamilton, Ontario, Canada, L8K 3P1",
    "51, Dydzak, Court, Dydzak Court, Hamilton, City of Hamilton, Ontario, Canada, L9B 1W1",
    "68, Hepburn, Crescent, Hepburn Crescent, Hamilton, City of Hamilton, Ontario, Canada, L9C 7S5",
    "268, Hunter, Street, West, Hunter Street West, Hamilton, City of Hamilton, Ontario, Canada, L8P 1S3",
    "110, Hanover, Place, Hanover Place, Hamilton, City of Hamilton, Ontario, Canada, L8K 5X6",
    "49, Upper Lake, Avenue, Upper Lake Avenue, Stoney Creek, City of Hamilton, Ontario, Canada, L8G 2V3",
    "58, Orr, Crescent, Orr Crescent, Stoney Creek, City of Hamilton, Ontario, Canada, L8G 5C5",
    "692, Concession 8, West, Concession 8 West, Flamborough, City of Hamilton, Ontario, Canada, N0B 2J0",]

    names = []
    emails = []
    password = "password"
    school = "University of Waterloo"
    for i in range(len(addresses)):
        fake = faker.Faker()
        name = fake.name()
        names.append(name)
        emails.append(f"{name.replace(' ', '.')}@gmail.com")

    for i in range(len(emails)):
        dh.register(names[i], emails[i], password, addresses[i], school)

    return "Hello world"


def generate_routes():
    global routes

    # Create new routes

    all_addrs = dh.get_addrs()
    with open(r"./Addresses.txt", "w+") as f:
        for addr in all_addrs:
            f.write(f"{addr}\n")


    r = rh.get_routes()
    routes = r

def generate_maps():
    global routes
    
    t = []
    for route in routes:
        temp = route.replace("899+Nebo+Rd,+Hannon,+ON+L0R+1P0,+Canada/", "")
        x = temp[:32] + "899+Nebo+Rd,+Hannon,+ON+L0R+1P0,+Canada/" + temp[32:]
        t.append(x)
    routes = t

    print(routes)

    for route in routes:
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) as driver: 
            driver.get(route)
            # Scroll down till the end
            driver.find_element(By.CSS_SELECTOR, ".yra0jd").click()
            specific_element = driver.find_element(By.CSS_SELECTOR, "canvas.aFsglc:nth-child(1)")
            actions = ActionChains(driver)
            actions.move_to_element(specific_element).perform()
            # Take a screenshot of just the located element and save it to a file
            driver.implicitly_wait(.719)
            specific_element.screenshot(f'static/vendor/maps/route{routes.index(route) + 1}.png')
        
        
            # Close the browser

            driver.quit()


if __name__ == "__main__":
    routes = []

    # generate routes
    if not generated_routes:
        generate_routes()
        generate_maps()

        generated_routes = True

    app.run()