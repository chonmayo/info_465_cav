import request
import create_map as cm
import distance as dist
import db_conn as db
import json


#ArcGIS supports GeoCoding for addresses
x = input("Enter coordinates for organ delivery\nlon: ")
y = input("lat: ")
#could be optional if you make a default constructor
name = input("Enter name of hospital: ")
blood_type = '\'{str}\''.format(str=input("Enter recipient information\nBlood type: "))
organ_t = '\'{str}\''.format(str=input("Enter organ type: "))
age = input("Enter recipient age: ")
print(blood_type)
print(organ_t)
#Organ life lookup
organ_hours = {
    'heart':16,
    'lung':8
}

organ_life = organ_hours[organ_t[1:-1].lower()]

recipient = request.Location(x,y,name)
locations = []
locations.append(recipient)
#the accident
incidents = (request.craft_json(locations))
locations.clear()
#the Location objects fetched from the V2X db
locations = db.Read(organ_t,blood_type,age)
facilities = (request.craft_json(locations))
response = request.send_post(incidents, facilities,organ_life)

#convert json to a dict
res_dict = json.loads(response.content)
"""
#mapoptions are returned in routes->features->directions->envelope
Geometry is located in routes->features->geometry
"""

route = res_dict['routes']['features'][0]['geometry']
envelope = res_dict['directions'][0]['summary']['envelope']

best_point = dist.optimize_route(route)
print(best_point['lon'])
best_point_geo={"paths":[[[best_point['incident_lon'],best_point['incident_lat']],[best_point['lon'],best_point['lat']],]]}
#send the route to create_map to change dict->json and send request
response = cm.craft_request(route,envelope,best_point_geo)
#DONE!!!!


example_donor = {
    'Donor_id':3,
    'Donor_name':'\'LLoyd\'',
    'Donor_age':48,
    'Donor_blood_type':'\'B\''
}

example_organ = {
    'Organ_id':3,
    'Hospital_id':2,
    'Donor_id':3,
    'Organ_type':'\'Heart\'',
    'Organ_life_hrs':16
}

example_geometry = {
"paths":[
[
    [
    -118.25736393499994,
    34.076763573000051
    ],
    [
    -118.25735999999995,
    34.076770000000067
    ],
    [
    -118.25779999999997,
    34.076950000000068
    ]
]
]
}