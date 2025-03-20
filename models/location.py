import json

class Location:
    def __init__(self, venue_latitude: float, venue_longitude: float):
        self.venue_latitude = venue_latitude #venue's latitude
        self.venue_longitude = venue_longitude #venue's longitude

    def to_dict(self):
        return {
            "venue_latitude": self.venue_latitude,
            "venue_longitude": self.venue_longitude
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)
