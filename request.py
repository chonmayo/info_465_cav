import json as j
import requests

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
#travelMode
#defaultCutoff - can cut off trip if it exceeds organ life
#barriertype allows you to set polygonal barriers
#defaultTargetFacilityRoute could be used in the future to calculate contingent routes
#travelDirection:esriNATravelDirectionFromFacility
#a location for where the organ is needed
#attributeParameterValues ['attributeName':'Driving an Emergency Vehicle', 'parameterName':'Restriction Usage', 'value':'Prohibited']
def send_post(incidents, facilities):
    token = "gixB1j9_B1nrzJaeg1p2Tn7-1SadhP_TsZ7BPevU6dkDzlXRmeET34QiyIyEvrruPfd75EIsOXFJbPxkVrIkmtREp39pkxnTAeDwGkSyWWdI1ORbbj5XzTkmO778bgdZOo1EFUm6ngA3GXgV_pIDLA.."
    url = "https://route.arcgis.com/arcgis/rest/services/World/ClosestFacility/NAServer/ClosestFacility_World/solveClosestFacility"

    payload = {'f':'json', 
        'token':token, 
        'returnDirections':'true',
        'returnCFRoutes':'true',
        'incidents':incidents,
        'facilities':facilities,
        }

    r = requests.post(url, data=payload)
    return r