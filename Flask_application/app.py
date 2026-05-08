from flask import Flask, request, render_template
from datetime import datetime
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client.test
collection = db["flask-tutorial"]

app = Flask("__name__")

@app.route("/")
def homepage():
    day_of_the_week = datetime.today().strftime("%A")
    currrent_time = datetime.now().strftime("%H:%M:%S")
    return render_template("index.html", day_of_the_week=day_of_the_week, current_time=currrent_time)

@app.route("/submit", methods=["POST"])
def submit():
    try:
        form_data = dict(request.form)
        status = collection.insert_one(form_data)

        day_of_the_week = datetime.today().strftime("%A")
        currrent_time = datetime.now().strftime("%H:%M:%S")
        return "Data submitted successfully" if status.acknowledged==True else render_template("error.html", day_of_the_week=day_of_the_week, current_time=currrent_time)
    except:
        day_of_the_week = datetime.today().strftime("%A")
        currrent_time = datetime.now().strftime("%H:%M:%S")
        return render_template("error.html", day_of_the_week=day_of_the_week, current_time=currrent_time)

@app.route("/view")
def view():
    data = collection.find()
    data = [dict(item) for item in data]
    for item in data:
        del item["_id"]
    return {"data": data}

@app.route("/api")
def view_from_file():
    with open("requirements.txt", "r") as file:
        data = file.readlines()
    return {"data": data}

@app.route("/todo")
def todo():
    day_of_the_week = datetime.today().strftime("%A")
    currrent_time = datetime.now().strftime("%H:%M:%S")
    return render_template("todo.html", day_of_the_week=day_of_the_week, current_time=currrent_time)

@app.route("/submittodo")
def submittodo():
    try:
        form_data = dict(request.form)
        status = collection.insert_one(form_data)
        return "Data submitted successfully" if status.acknowledged==True else "Data could not be submitted"
    except:
        return "Data could not be submitted"


if __name__ == "__main__":
    app.run(debug=True)

