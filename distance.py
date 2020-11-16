from math import radians, cos, sin, asin, sqrt

#if it is ever more efficient to use a drone at a point in the route, calculate distance to point
#pop the step from direstions and amend the route to 

def haversine_distance(lon1, lat1, lon2,lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
geometry = {
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
    ],
    [
    -118.25799999999998,
    34.077040000000068
    ],
    [
    -118.25873999999999,
    34.077360000000056
    ],
    [
    -118.25900999999999,
    34.077480000000037
    ],
    [
    -118.25941999999998,
    34.077660000000037
    ]
]
]
}
path = geometry['paths'][0]
route_incremental_distance = 0
best_point = {
    'lon':path[-1][0],
    'lat':path[-1][1],
    'time_saved':0
}

#MOVE TO CONFIG
DRONE_MAX_MILE = 15
UAV_AVG_SPEED = 30#mph
AMB_AVG_SPEED = 35#mph

for index in reversed(range(0,len(path)-1)):
    #the lon and lat of the incident
    lon0 = path[-1][0]
    lat0 = path[-1][1]
    #the lon and lat of a previous point
    lon1 = path[index+1][0]
    lat1 = path[index+1][1]
    #the lon and lat of a new point
    lon2 = path[index][0]
    lat2 = path[index][1]
    incident_distance = haversine_distance(lon0,lat0,lon2,lat2)
    route_incremental_distance += haversine_distance(lon1,lat1,lon2,lat2)
    print("incident d:{id}\troute d:{rd}".format(id=incident_distance, rd=route_incremental_distance))
    #calculate efficiency
    if(incident_distance<DRONE_MAX_MILE):
        amb_time = route_incremental_distance/AMB_AVG_SPEED
        uav_time = incident_distance/UAV_AVG_SPEED
        eff = uav_time-amb_time
        print(eff)
        if(eff>best_point['time_saved']):
            best_point['lon']=lon2
            best_point['lat']=lat2
            best_point['time_saved']=eff
print(best_point)