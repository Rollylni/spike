import datetime
import requests
import config
import pytz
import json


def log(msg, level="info"):
    """
    :type msg: str
    :type level: str
    """
    now = datetime.datetime.utcnow()
    utc = now.replace(tzinfo=pytz.utc)
    msc_time = utc.astimezone(pytz.timezone("Europe/Moscow"))
    print(msc_time.strftime("%H:%M:%S") + " [" + level.upper() + "] " + msg)
    
    
def method(method, params):
    """
    :param method: vk api method
    :type method: str
    
    :param params: method parameters
    :type params: dict
    """
    if "v" not in params:
        params["v"] = config.VERSION
        
    if "access_token" not in params:
        params["access_token"] = config.TOKEN
        
    if "lang" not in params:
        params["lang"] = config.LANG
        
    response = requests.post('https://api.vk.com/method/' + method, params)
    
    if response.ok:
        response = response.json()
    else:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err_msg:
            log("Method " + method + " failed!")
            log("HTTP: " + err_msg, "error")
            return []
    
    if "error" in response:
        log("Method " + method + " failed!") 
        log("VK-API: " + response["error"]["error_msg"], "error")
    
    if "response" in response:
        return response["response"]
        
    return response
        
  
def get_user(users, fields="sex,online"):
    return method("users.get", {
        "user_ids": str(users),
        "fields": fields
    })
    
def send_msg(peer_id, message, keyboard=None):
    params = {
        "peer_id": str(peer_id),
        "message": str(message),
        "random_id": 0
    }
    
    if keyboard is not None:
        params["keyboard"] = keyboard
        
    method("messages.send", params)
    
class Keyboard:
    """
    :param one_time: bool
    :param inline: bool
    """
    def __init__(self, one_time=True, inline=False):
        self.inline = inline
        self.one_time = one_time
        self.buttons = [[]]
        
    def get_body(self):
        """
        :returns: str
        """
        return json.dumps({
            "one_time": self.one_time,
            "buttons": self.buttons,
            "inline": self.inline},
            ensure_ascii=False,
            separators=(",", ":"))
            
    def remove_keyboard(self):
        self.buttons = []
        return self.get_body()
        
    def add_button(self, label, color, payload=None):
        """
        :param label: str
        :param color: str
        :param payload: str
        """
        line = self.buttons[-1]
        line.append({
            'color': color,
            'action': {
                'type': "text",
                'payload': payload,
                'label': label,
            }
        })
    
    def add_line(self):
        self.buttons.append([])
        

class LongPoll:
    """
    :param group_id: int
    """
    def __init__(self, group_id=None):
        self.id = config.GROUP_ID if group_id is None else group_id
        self.wait = config.WAIT
        self.ts = None
        self.key = None
        self.server = None
        
    def session(self):
        response = method("groups.getLongPollServer", {
            "group_id": self.id
        })
        self.server = response["server"]
        self.key = response["key"]
        self.ts = response["ts"]
            
    def get_events(self):
        params = {
            'act': 'a_check',
            'key': self.key,
            'ts': self.ts,
            'wait': self.wait,
        }
        
        response = requests.get(self.server, params=params).json()
        
        if "failed" in response:
            if response["failed"] == 1:
                self.ts = response["ts"]
            else:
                self.session()
            return []
        else:
            self.ts = response["ts"]
            return response["updates"]