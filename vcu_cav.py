import request
import create_map as cm
import response_processing as rp

#ArcGIS supports GeoCoding for addresses
x = input("Enter coordinates for organ delivery\nx: ")
y = input("y: ")
#could be optional if you make a default constructor
name = input("Enter name of hospital: ")
blood_type = input("Enter recipient information\nBlood type: ")
organ = input("Enter organ type: ")
age = input("Enter recipient age: ")

recipient = request.Location(x,y,"4326", name)
#recipient = request.Location(-118.257363, 34.076763, "4326", "Echo Park Ave & W Sunset Blvd, Los Angeles, California, 90026")
locations = []
locations.append(recipient)
#reverse routing fromfacilitytoevent
#the accident
incidents = (request.craft_json(locations))
locations.clear()
#the hospital objects fetched from the database
#locations.append(DB_VALUES)
features = (request.craft_json(locations))
response = request.send_post(incidents, features)

#convert json to a dict
metadaddy = rp.json_to_dict(response.content)

#select the features we need from the dict
metadaddy = rp.grep_route(metadaddy)

#send the route to create_map to change dict->json and send request
response = cm.craft_request(metadaddy)
metadaddy = rp.json_to_dict(response.content)

#wget the url provided in the response
#sys.exec("wget {url}".format(url=metadaddy['url']))
#open the png file

#DONE!!!!