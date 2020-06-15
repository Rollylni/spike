import requests
import config
import utils
import json

class BrawlApi:
    """
    :ivar obj: method response
    :type obj: dict
    """
    obj = {}
    
    def method(self, method):
        """
        :param method: bs-api method
        :type method: str
        
        :returns: requests.Response()
        """
        header = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + config.BS_API_KEY
        }
        
        try:
            response = requests.get("https://api.brawlstars.com/v1/" + method, headers=header)
            if not response.ok:
                response.raise_for_status()
        except requests.exceptions.HTTPError: 
            utils.log("BS-API: Method " + method + " failed", "error")
        return response
    
    def get(self, key):
        """
        :param key: 
        :type key: str
        
        :returns: Value|None
        """
        if key in self.obj:
            return self.obj[key]
        else:
            return None
    
class Player(BrawlApi):
    
    def __init__(self, tag):
        try:
            self.obj = self.method("players/" + tag).json()
        except json.decoder.JSONDecodeError:
            self.obj = []
        
class Club(BrawlApi):
    
    def __init__(self, tag):
        try: 
            self.obj = self.method("clubs/" + tag).json()
        except json.decoder.JSONDecodeError:
            self.obj = []