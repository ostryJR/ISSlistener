
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
    latitude = None
    longitude = None
    name = None
    country = None
    webSDRurl = None
    
    def __init__(self, latitude, longitude, name, country, webSDRurl):
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.country = country
        self.webSDRurl = webSDRurl

class blablabla:
    def __init__(self):
        pass