
class FlyoverFrame:
    date = None
    starttime = None
    duration = None
    endtime = None
    
    def __init__(self, date, starttime, duration, endtime):
        self.date = date
        self.starttime = starttime
        self.duration = duration
        self.endtime = endtime


class Location:
    name = None
    country = None
    webSDRurl = None
    latitude = None
    longitude = None
    square = None
    
    def __init__(self, name, country, webSDRurl, latitude, longitude, square):
        self.name = name
        self.country = country
        self.webSDRurl = webSDRurl
        self.latitude = latitude
        self.longitude = longitude
        self.square = square
