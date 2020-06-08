import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
# SQLALCHEMY_TRACK_MODIFICATIONS gets rid of the SQLAlchemy message that displays everytime I run the server
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route('/')
def index_get():
    # Variable that holds all the cities in my sqlite3 database table -> is a query from the City table
    cities = City.query.all()
    # OpenWeatherMap API url
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=a95bbf99e1761eac5543637aac409d6e'
    # # Temporary test data
    # city = 'Los Angeles'

    # list to hold the weather for all the cities
    weather_data = []

    for city in cities:

        # Requesting info from weatherAPI. 'url.format(city)' inserts my 'city' variable into the {} inside url variable.
        # r => all data included in the API
        r = requests.get(url.format(city.name)).json()
        print(r)

        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        # Append the requested data into the weather_data list
        weather_data.append(weather)
        # Display requested data in terminal to test out server
        print(weather)

    return render_template('weather.html', weather_data=weather_data)

@app.route('/', methods=['POST'])
def index_post():
    err_msg = ''
    new_city = request.form.get('city')

    # Check if user input a city
    if new_city:
        # Declare a variable to grab/hold the city IF it already exists in database == City already exists
        existing_city = City.query.filter_by(name=new_city)

        # If the city does not already exist...
        if not existing_city:
            new_city_obj = City(name=new_city)

            # Add city to database as an object
            db.session.add(new_city_obj)
            # Confirm changes
            db.session.commit()

        # If the city already exists...
        else:
            # Send error message instead...
            err_msg = 'City already exists!!!'

    # redirect takes user back to the desired route
    return redirect(url_for('index_get'))