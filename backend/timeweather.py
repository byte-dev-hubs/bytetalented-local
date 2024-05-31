from datetime import datetime
from pytz import country_timezones, country_names
from timezonefinder import TimezoneFinder
from utils.city_cords import city_cords
from taipy.gui import notify
from threading import Timer
from flask import current_app, Flask
from model.usercity import Usercity
import asyncio
import pytz
import requests
import time

app = Flask(__name__)
city_data = []
cities = []
weather_icons=""
selected_city = None
show_add_time_dialog = False
timer_flag = False
city_count = 0

def load_time_weather(state):
    user_cities = Usercity.getUserCityByUserId(state.user_id)
    if not user_cities:
        return
    new_city_data = state.city_data.copy()
    index = 0
    
    for city in user_cities:
        city_name = city[2]
        city_country = city[3]
        timezone = city[4]
        weather = fetch_weather(city_name)
        now = datetime.now(pytz.timezone(timezone))
        new_city_data[index] = {
        "city": city_name,
        "country": city_country,
        "timezone": timezone,
        "time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "weather": weather
        }   
        index += 1
    state.city_data = new_city_data
    state.city_count = index
    return

def on_init(state):
    clock_data = {
        'city': 'San Fransisco', 
        'country': 'USA', 
        'timezone': 'America/Los_Angeles',   
        'time': '2024-05-30 13:05:51', 
        'weather': {
            'description': 'few clouds', 
            'temperature': 23.11, 
            'humidity': 58, 
            'wind_speed': 7.72, 
            'icon': '02d'
        }
    }
    icon_data = "https://openweathermap.org/img/wn/04n@2x.png"
    
    state.city_data = [clock_data] * 5
    state.weather_icons=[icon_data] * 5
    state.city_count = 0
    
    
    state.cities = get_all_cities()
    state.selected_city = None
    

def update_all_city_data(state):
    while True:
        index = 0
        new_city_data = state.city_data.copy()
        for data in new_city_data:
            now = datetime.now(pytz.timezone(data["timezone"]))
            new_city_data[index]["time"] = now.strftime("%Y-%m-%d %H:%M:%S")
            index += 1
        state.city_data = new_city_data
        time.sleep(1)
    # Trigger a state update
    

def start_timer(state):
    # Define a function to repeatedly call update_all_city_data
    update_all_city_data(state)

def fetch_weather(city):
    api_key = "00159dd6e4efdcc48a08f1be868ed801"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    weather = {
        "description": data["weather"][0]["description"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "icon": data["weather"][0]["icon"]
    }
    return weather


def do_add_city(state, city_info):
    city_key, display_label = city_info
    country, city = city_key.split('/')
    city_data = next((item for item in city_cords[country] if item['city'] == city), None)
    
    if not city_data:
        notify(state, "E", f"City {city} in {country} not found in coordinates data")
        return
    
    tf = TimezoneFinder()
    lat = city_data['lat']
    lon = city_data['lon']
    timezone_str = tf.timezone_at(lat=lat, lng=lon)
    if timezone_str is None:
        notify(state, "E", f"Could not determine timezone for {city}")
        return
    if not Usercity(user_id=state.user_id, city=city, country=country, timezone=timezone_str).insert_new_city():
        return notify(state, "W", f"City {city} in {country} already exists in the list")
    now = datetime.now(pytz.timezone(timezone_str))
    weather = fetch_weather(city)
    new_weather_icons = state.weather_icons.copy()
    new_weather_icons[state.city_count] = f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png"
    
    new_city_data = state.city_data.copy()
    new_city_data[state.city_count] = {
        "city": city,
        "country": country,
        "timezone": timezone_str,
        "time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "weather": weather
    }
    state.city_data = new_city_data
    state.weather_icons = new_weather_icons
    state.city_count += 1
    
    notify(state, "S", f"Added {city} in {country} to the list")
    return
    
def get_all_cities():
    cities = []
    tf = TimezoneFinder()
    for country, city_list in city_cords.items():
        seen_timezones = set()
        for city_info in city_list:
            lat, lon = city_info['lat'], city_info['lon']
            timezone_str = tf.timezone_at(lat=lat, lng=lon)
            if timezone_str not in seen_timezones:
                seen_timezones.add(timezone_str)
                city_info['timezone'] = timezone_str
                cities.append((city_info['country'] + '/' + city_info['city'],city_info['city'] + ", " + city_info['country'] + " (" + timezone_str + ")"))
    return cities

    
def on_add_time_finish(state, action, payload):
    if payload['args'][0] == 0:
        do_add_city(state, state.selected_city)
        state.show_add_time_dialog = False
    else:
        state.show_add_time_dialog = False
    return

def on_btn_add_time_zone_clicked(state, action, payload):
    state.show_add_time_dialog = True
    return

def remove_timezone(state, id):
    print(state, id)
    return