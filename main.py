import json
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
import os
from dotenv import load_dotenv
import requests

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
DATA_FILE = Path("restaurants.json")

def load_restaurants():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []

def save_restaurants(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))

def get_coordinates(address: str):
    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params={"address": address, "key": GOOGLE_MAPS_API_KEY})
    data = response.json()
    if data["results"]:
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None, None

class Category(str, Enum):
    restaurant = "Restaurant"
    cafe = "Café"
    bar = "Bar"
    fastfood = "Fastfood"
    point_of_interest = "Point of interest"

class Restaurant(BaseModel):
    id: int
    name: str
    category: Category
    cuisine: str
    location: str
    rating: float | None = None
    note: str | None = None
    lat: float | None = None
    lng: float | None = None

app = FastAPI()

restaurants = load_restaurants()
next_id = max((r["id"] for r in restaurants), default=0) + 1

@app.get("/restaurants")
async def get_restaurants():
    return restaurants

# Needs to be updated as well
@app.get("/restaurants/{restaurant_id}")
async def get_restaurant(restaurant_id):
    return {"restaurant_id": restaurant_id}


@app.post("/restaurants")
async def create_restaurant(restaurant: Restaurant):
    global next_id
    restaurant.id = next_id
    next_id += 1
    restaurant.lat, restaurant.lng = get_coordinates(restaurant.location)
    restaurants.append(restaurant.model_dump())
    save_restaurants(restaurants)
    return restaurant


@app.put("/restaurants/{restaurant_id}")
async def update_restaurant(restaurant_id: int, updated: Restaurant):
    for i, r in enumerate(restaurants):
        if r["id"] == restaurant_id:
            updated.lat, updated.lng = get_coordinates(updated.location)
            restaurants[i] = updated.model_dump()
            save_restaurants(restaurants)
            return updated
    return {"error": "Restaurant ikke fundet"}


@app.delete("/restaurants/{restaurant_id}")
async def delete_restaurant(restaurant_id: int):
    global restaurants
    restaurants = [r for r in restaurants if r["id"] != restaurant_id]
    save_restaurants(restaurants)
