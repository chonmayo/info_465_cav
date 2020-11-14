import json as j
import requests

class Location:
    def __init__(self,x,y,wkid,name):
        self.x = x
        self.y = y
        self.wkid = wkid
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
def send_post(incidents, features):
    token = "hlZGd_2-fcUTB_bNs1D4YJyn28i0UmcHiFbCJs7xuu_laVGYbBmu7ZgE2G1rbFUU9p1RyYf-CtPrNMlx68UEGqr0FAwI8tPkOWRA4qF-TyTfVe7exnA2UR0c99j4XcahCPgxdZjWV4_Tl4ORTpWexw.."
    url = "https://route.arcgis.com/arcgis/rest/services/World/ClosestFacility/NAServer/ClosestFacility_World/solveClosestFacility"

    payload = {'f':'json', 
        'token':token, 
        'returnDirections':'true',
        'returnCFRoutes':'true',
        'incidents':incidents,
        'features':features,
        }

    r = requests.post(url, data=payload)
    return r