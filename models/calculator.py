from math import radians, sin, cos, sqrt, atan2
from models.order import Order

class DeliveryCalculator:
    def __init__(self, base_price, a, b, min_cart_value, max_distance):
        self.base_price = base_price #Default delivery cost
        self.a = a #Constant additional amount
        self.b = b #Multiplier for calculating distance
        self.min_cart_value = min_cart_value #Minimum cart value
        self.max_distance = max_distance #Maximum delivery distance

    def calculate_distance(self, order: Order):
        #Distance Calculator between user and venue based on Haversine Formula

        R = 6371008 #Average radius of the Earth in meters

        #Since the Earth's radius varies due to its imperfect spherical shape—ranging
        #from 6356.752 km at the poles to 6378.137 km at the equator
        #=> the average radius of 6371.008 km is used in the calculation.

        user_lat_rad = radians(order.user_latitude)
        user_lon_rad = radians(order.user_longitude)
        venue_lat_rad = radians(order.venue_location.venue_latitude)
        venue_lon_rad = radians(order.venue_location.venue_longitude)

        #Difference Calculator between user and venue
        dist_lat = user_lat_rad - venue_lat_rad
        dist_lon = user_lon_rad - venue_lon_rad

        #The Haversine Formula
        # --------------------
        # the source: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
        a = sin(dist_lat / 2) ** 2 + cos(user_lat_rad) * cos(venue_lat_rad) * sin(dist_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        #Distance in meters
        distance = int(R * c)
        if distance > self.max_distance:
            raise ValueError("Delivery distance exceeds the maximum allowed distance.")
        return distance

    def calculate_delivery_fee(self, distance):
        #Delivery Calculator Implementation
        delivery_fee = self.base_price + self.a + self.b * (distance / 10)
        return int(delivery_fee)

    def calculate_small_order_surcharge(self, cart_value):
        #small order surcharge Calculator Implementation
        return max(0, self.min_cart_value - cart_value)

    def calculate_total(self, order):
        # Main logic for total_price Calculator
        distance = self.calculate_distance(order)
        delivery_fee = self.calculate_delivery_fee(distance)
        small_order_surcharge = self.calculate_small_order_surcharge(order.cart_value)
        total_price = order.cart_value + delivery_fee + small_order_surcharge

        return {
            "total_price": total_price,
            "small_order_surcharge": small_order_surcharge,
            "cart_value": order.cart_value,
            "delivery": {
                "fee": delivery_fee,
                "distance": distance,
            }
        }
