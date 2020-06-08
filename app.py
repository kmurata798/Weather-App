import requests
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 
app.config['DEBUG'] = True

@app.route('/')
def index():
    # OpenWeatherMap API url
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=a95bbf99e1761eac5543637aac409d6e'
    # Temporary test data
    city = 'Las Vegas'

    # Requesting info from weatherAPI. 'url.format(city)' inserts my 'city' variable into the {} inside url variable.
    r = requests.get(url.format(city)).json()
    print(r)
    return render_template('weather.html')





# if __name__ == '__main__': 
#     app.run(debug = True) 