import json
from math import radians, cos, sin, asin, sqrt


def json_to_dict(response):
    """
    deserialize json to dictionary object
    """
    js = response
    _dict = json.loads(js)

    return _dict


def grep_url(url):
    return url

#if it is ever more efficient to use a drone at a point in the route, calculate distance to point
#pop the step from direstions and amend the route to 
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r