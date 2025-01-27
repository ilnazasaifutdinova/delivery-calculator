import json
from models.location import Location

class Order:
    def __init__(self, venue_slug: str, cart_value: int, user_latitude: float, user_longitude: float):
        self.venue_slug = venue_slug #venue ID
        self.cart_value = cart_value #Cart cost
        self.user_latitude = user_latitude #User's latitude
        self.user_longitude = user_longitude #User's longitude
        self.venue_location = None

    def set_location(self, location: Location):
        if not isinstance(location, Location):
            raise TypeError("location must be an instance of Location")
        self.venue_location = location

    def to_dict(self):
        return {
            "venue_slug": self.venue_slug,
            "cart_value": self.cart_value,
            "user_latitude": self.user_latitude,
            "user_longitude": self.user_longitude,
            "venue_location": self.venue_location.to_dict() if self.venue_location else None,
        }

    def __repr__(self):

        return json.dumps(self.to_dict(), indent=4)
