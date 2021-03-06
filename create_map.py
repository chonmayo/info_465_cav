import requests
import json
"""

#mapoptions are returned in routes->features->directions->envelope
Geometry is located in routes->features->geometry

"""

def craft_request(geometry,envelope,best_point_geo):
  
  map_dict = {
      
      'mapOptions': {
      "extent": {
        "xmin": envelope['xmin']-0.3,
        "ymin": envelope['ymin']-0.3,
        "xmax": envelope['xmax']+0.3,
        "ymax": envelope['ymax']+0.3,
        "spatialReference": {
          "wkid": 4326
          }
        }
      },
    "operationalLayers": [
      {
        "opacity":1,
        "featureCollection": {
          "layers": [
            {
              "layerDefinition": {
                "name": "AmbLayer",
                "geometryType": 'esriGeometryPolyline',
                "drawingInfo": {
                  "renderer": {
                    "type": "simple",
                    "symbol": {
                        "type" :"esriSLS",
                        "style":"esriSLSDot",
                        "color":[0,0,0],
                        "width": "5"
                      }
                    }
                  }
                },
                "featureSet": {
                "features": [
                  {
                    "geometry":geometry,
                    "spatialReference":{"wkid": 4326}
                  }
                ]
              }
            },
            {
              "layerDefinition": {
                "name": "UAVLayer",
                "geometryType":'esriGeometryPolyline',
                "drawingInfo": {
                  "renderer": {
                    "type": "simple",
                    "symbol": {
                        "type" :"esriSLS",
                        "style":"esriSLSSolid",
                        "color":[255,0,0],
                        "width": "5"
                      }
                    }
                  }
                },
                "featureSet": {
                "features": [
                  {
                    "geometry":best_point_geo,
                    "spatialReference":{"wkid": 4326}
                  }
                ]
              }
            }
          ]
        }
      }
    ],
    #BaseMap stays the same
    "baseMap" : {
      "title" : "Topographic Basemap",
      "baseMapLayers" :  [
        {
          "url" : "https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer"
        }
      ]
    },
    #export options stays the same
    "exportOptions": {
      "outputSize" :  [600,400]
    }
  }

  json_data = json.dumps(map_dict, indent=4)
  url = "https://utility.arcgisonline.com/arcgis/rest/services/Utilities/PrintingTools/GPServer/Export Web Map Task/execute"

  payload = {
    'f':'json',
    'Format':'PNG32',
    'Layout_Template':'MAP_ONLY',
    'Web_Map_as_JSON':json_data
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  response = requests.request("POST", url, headers=headers, data = payload)
  print(response)
  #parse url from response and download the file
  response_dict = json.loads(response.content)
  url = response_dict['results'][0]['value']['url']
  r = requests.get(url, allow_redirects=True)
  open('map.png', 'wb').write(r.content)

  return(response)