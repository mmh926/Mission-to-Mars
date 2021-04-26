# Lets break down what this code is doing.

# The first line says that we'll use Flask to render a template, redirecting to another url,
# and creating a URL.
# The second line says we'll use PyMongo to interact with our Mongo database.
# The third line says that to use the scraping code, we will convert from Jupyter 
# notebook to Python.
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Add the following to set up Flask:
app = Flask(__name__)

# Tell Python how to connect to Mongo using PyMongo.
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the HTML page.
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

 # Our next function will set up our scraping route. This route will be the 
 # "button" of the web application, the one that will scrape updated data when 
 # we tell it to from the homepage of our web app. It'll be tied to a button 
 # that will run the code when it's clicked. 
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

# Update the database 
# Finally, the option we'll include is upsert=True. This indicates to Mongo to 
# create a new document if one doesn't already exist, and new data will always 
# be saved (even if we haven't already created a document for it).

# Add a redirect after successfully scraping the data:
# This will navigate our page back to / where we can see the updated content.
# return redirect('/', code=302)

# We need for Flask is to tell it to run. Add these two lines to the bottom of 
# your script and save your work:
if __name__ == "__main__":
   app.run()