from fastapi import APIRouter, HTTPException
import requests
from models.location import Location
from models.calculator import DeliveryCalculator
from models.order import Order

router = APIRouter()

def fetch_static_data(venue_slug: str) -> Location:
    static_url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/static"
    response = requests.get(static_url)

    #Checking response status
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Static API data not found")

    static_data = response.json()

    #Path to coordinates checking
    try:
        coordinates = static_data["venue_raw"]["location"]["coordinates"]
        venue_lon, venue_lat = coordinates  # longitude, latitude
    except KeyError:
        raise HTTPException(status_code=500, detail="Missing 'coordinates' in Static API data")

    #Location creating
    return Location(venue_latitude=venue_lat, venue_longitude=venue_lon)

def fetch_dynamic_data(venue_slug: str) -> dict:
    dynamic_url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/dynamic"
    response = requests.get(dynamic_url)

    #Checking response status
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Dynamic API data not found")

    dynamic_data = response.json()

    #Import certain data
    try:
        delivery_specs = dynamic_data["venue_raw"]["delivery_specs"]
        min_cart_value = delivery_specs["order_minimum_no_surcharge"]
        base_price = delivery_specs["delivery_pricing"]["base_price"]

        #Import distance ranges
        distance_ranges = delivery_specs["delivery_pricing"]["distance_ranges"]
        max_distance = max(range["to"] for range in distance_ranges if "to" in range)
        a = distance_ranges[0]["price"]  # Цена для минимального расстояния
        b = distance_ranges[1]["price"] - distance_ranges[0]["price"]  # Разница между первым и вторым диапазоном
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Missing key in Dynamic API data: {str(e)}")

    return {
        "min_cart_value": min_cart_value,
        "base_price": base_price,
        "a": a,
        "b": b,
        "max_distance": max_distance,
    }

@router.get("/api/v1/delivery-order-price")
def calculate_delivery(
    venue_slug: str,
    cart_value: int,
    user_latitude: float,
    user_longitude: float
):
    try:
        #Import data from Static API
        venue_location = fetch_static_data(venue_slug)

        #Import Data from Dynamic API
        dynamic_data = fetch_dynamic_data(venue_slug)

        #Creating Order object
        order = Order(
            venue_slug=venue_slug,
            cart_value=cart_value,
            user_latitude=user_latitude,
            user_longitude=user_longitude
        )
        order.set_location(venue_location)

        #Creating DeliveryCalculator object
        calculator = DeliveryCalculator(
            base_price=dynamic_data["base_price"],
            a=dynamic_data["a"],
            b=dynamic_data["b"],
            min_cart_value=dynamic_data["min_cart_value"],
            max_distance=dynamic_data["max_distance"]
        )

        #Calculating FinalCost
        result = calculator.calculate_total(order)
        return result

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
