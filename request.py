import json as j
import requests
import config

class Location:
    def __init__(self,x,y,name):
        self.x = y
        self.y = x
        self.wkid = 4326
        self.name = name

def craft_json(locations):
    features = []
    ret = {}
    for location in locations:
        spatial = {'wkid':location.wkid}
        geometry = {
            'x':location.x,
            'y':location.y,
            'spatialReference':spatial
        }
        attributes = {
            'Name':location.name
        }
        features.append({
            'geometry':geometry,
            'attributes':attributes
        })
    ret['features'] = features
    json = j.dumps(ret,indent = 4)
    return json

#you can use synchronous execution mode
#barriertype allows you to set polygonal barriers
#defaultTargetFacilityRoute could be used in the future to calculate contingent routes
def send_post(incidents, facilities, organ_life_hours):
    url = "https://route.arcgis.com/arcgis/rest/services/World/ClosestFacility/NAServer/ClosestFacility_World/solveClosestFacility"

    payload = {'f':'json', 
        'token':config.token, #access token
        'returnDirections':'true', #return directions
        'returnCFRoutes':'true', #return routes
        'travelDirection':'esriNATravelDirectionFromFacility', #the route calculation begins from facilities
        'defaultCutoff':organ_life_hours, #the organs maximum travel time
        'incidents':incidents, #the location of the patient in need
        'facilities':facilities, #the hospitals with organs matching patient needs
        
        'attributeParameterValues':{ #does not include routes with roadways that prohibit emergency vehicles
            'attributeName':'Driving an Emergency Vehicle',
            'parameterName':'Restriction Usage',
            'value':'Prohibited'}
        }

    r = requests.post(url, data=payload)
    return r