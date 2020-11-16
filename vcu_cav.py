import request
import create_map as cm
import response_processing as rp
import db_conn as db


#ArcGIS supports GeoCoding for addresses
x = input("Enter coordinates for organ delivery\nx: ")
y = input("y: ")
#could be optional if you make a default constructor
name = '\'{str}\''.format(str=input("Enter name of hospital: "))
blood_type = '\'{str}\''.format(str=input("Enter recipient information\nBlood type: "))
organ = input("Enter organ type: ")
age = input("Enter recipient age: ")

#Organ life lookup
organ_hours = {
    'heart':16,
    'lung':8
}

organ_life = organ_hours[organ_t.lower()]

recipient = request.Location(x,y,name)
locations = []
locations.append(recipient)
#the accident
incidents = (request.craft_json(locations))
locations.clear()
#the Location objects fetched from the V2X db
locations = db.Read(name,blood_type,age)
facilities = (request.craft_json(locations))
response = request.send_post(incidents, facilities)

#convert json to a dict
res_dict = rp.json_to_dict(response.content)
"""
#mapoptions are returned in routes->features->directions->envelope
Geometry is located in routes->features->geometry
"""

route = res_dict['routes']['features'][0]['geometry']
envelope = res_dict['directions'][0]['summary']['envelope']

#send the route to create_map to change dict->json and send request
response = cm.craft_request(route,envelope)
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

