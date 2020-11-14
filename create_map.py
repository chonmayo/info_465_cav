import requests
import json
"""

#mapoptions are returned in routes->features->directions->envelope
Geometry is located in routes->features->geometry

"""

def craft_request(response):
  map_dict = {
      
      'mapOptions': {
      "extent": {
        "xmin": -118.85360990096176,
        "ymin": 33.99062491328014,
        "xmax": -118.75318799544432,
        "ymax": 34.04042561067984,
        "spatialReference": {
          "wkid": 4326
          }
        }
      },
    "operationalLayers": [
      {
        "opacity":0.35,
        "featureCollection": {
          "layers": [
            {
              "layerDefinition": {
                "name": "pointLayer",
                "geometryType": "esriGeometryPoint",
                "drawingInfo": {
                  "renderer": {
                    "type": "simple",
                    "symbol": {
                      "type": "esriSMS",
                      "style": "esriSMSCircle",
                      "color": [
                        255,
                        165,
                        194,
                        255
                      ],
                      "size": 50,
                      "outline": {
                        "color": [
                          255,
                          48,
                          144,
                          255
                        ],
                        "width": 3
                        }
                      }
                    }
                  }
                },
                "featureSet": {
                "features": [
                  {
                    "geometry": {
                      "x": -118.80619999999999,
                      "y": 34.00167000000005,
                      "spatialReference": {
                        "wkid": 4326
                      }
                    }
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

  return(response)