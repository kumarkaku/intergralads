import http.client 
import urllib.request
import urllib.parse
import urllib.error 
import base64
import json

class Trains:
    def __init__(self):
        self.line_code = "YL"
        self.ds_name = "Huntington"
        self.header = {"api_key":"e13626d03d8e4c03ac07f95541b3091b"}
        self.api_endpt = "api.wmata.com"
        self.ds_code = self.get_station_code()

    def get_station_code(self):
        params = urllib.parse.urlencode({ "LineCode": self.line_code })
        try:
            conn = http.client.HTTPSConnection(self.api_endpt)
            conn.request("GET", "/Rail.svc/json/jStations?%s" % params, "{body}", self.header)
            response = conn.getresponse()
            data = json.loads(response.read())
            stlist =  { element["Name"]:element["Code"] for element in data["Stations"] }
            conn.close()
            return (stlist[self.ds_name])
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def get_yl_running_trains_to_huntington(self):
        params = urllib.parse.urlencode({ })
        try:
            conn = http.client.HTTPSConnection(self.api_endpt)
            conn.request("GET", "/TrainPositions/TrainPositions?contentType={contentType}&%s" % params, "{body}", self.header)
            response = conn.getresponse()
            data = json.loads(response.read())
            
            # Filter all running trains on Yellow Line.
            data = [item for item in data["TrainPositions"] if item["LineCode"] == self.line_code]

            # Filter all running trains of ServiceType "Normal"
            data = [item for item in data if item["ServiceType"] == "Normal"]
        
            # Filter all running trains Whose Destination is "Huntington"
            data = [item for item in data if item["DestinationStationCode"] == self.ds_code]
            conn.close()
            return data
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
 

if __name__ ==  "__main__":
    train =  Trains()
    result = train.get_yl_running_trains_to_huntington()
    print(f"Total Number of trains heading towards Huntington: {len(result)}")
    if result:
       print(json.dumps(result, indent=2))
   
