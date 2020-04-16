from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import sys

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mission_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    Mars_dict = mongo.db.Mars_mission.find_one()
    return render_template("index.html", Mars_dict=Mars_dict)


@app.route("/scrape")
def scraper():
    Mars_dict = mongo.db.Mars_mission
    Mars_data = scrape_mars.scrape()
    Mars_dict.update({}, Mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
