import requests
import json

class LEDStrip:
    def __init__(self, name, host, port):
        self.host = host
        self.port = port
        self.name = name

    def setColor(self, red, green, blue):
        url = self.getUrl()
        data = {
            'red': red,
            'green': green,
            'blue': blue
        }


        response = requests.post(url, json=data)
        return response.status_code == 200

    def turnOff(self):
        url = self.getUrl()
        data = {
            'red': 0,
            'green': 0,
            'blue': 0
        }

        response = requests.post(url, json=data)
        return response.status_code == 200
    
    def getUrl(self):
        return 'http://{}:{}'.format(self.host, self.port)
    
    def getName(self);
        return self.name
