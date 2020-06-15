# author Rolly
from config import DEV_IDS, MESSAGES, WIDGET, DEV_TOKEN, TOPIC
from brawlstars import Player, Club
from json import loads, dumps
from threading import Thread
from time import time as ntime
import utils

utils.log("Бот запущен!")
long_poll = utils.LongPoll()
long_poll.session()

peer = None
life = True
time = ntime()
_time = ntime()

def send_msg(msg, keyboard=None):
    utils.send_msg(peer, msg, keyboard)
    
def isDev(user):
    if user in DEV_IDS:
        return True
    else:
        send_msg(MESSAGES["perm-denied"])
        return False
        
def getType(type):
    if type == "open":
        return "открытый"
    elif type == "closed":
        return "закрытый"
    else:
        return "по-приглашению"
        
def getRole(role):
    if role == "president":
        return "Президент"
    elif role == "vicePresident":
        return "Вице-президент"
    elif role == "senior":
        return "Ветеран"
    else:
        return "Участник"
        
def getClub(tag):
    club = Club(tag)
    keyboard = utils.Keyboard(False, True)
    msg = MESSAGES["club-def"]
    if club.get("name") is None:
        send_msg("Информация о клубе с тегом " + tag + " не найдена!")
    else:
        if club.get("description") is not None:
            msg = msg.replace("%description%", "\n" + str(club.get("description")))
        else:
            msg = msg.replace("%description%", "отсутствует!")
        msg = msg.replace("%tag%", club.get("tag").replace("%","#"))
        msg = msg.replace("%name%", str(club.get("name")))
        msg = msg.replace("%type%", getType(club.get("type")))
        msg = msg.replace("%requiredTrophies%", str(club.get("requiredTrophies")))
        msg = msg.replace("%trophies%", str(club.get("trophies")))
        msg = msg.replace("%members%", str(len(club.get("members"))))
        keyboard.add_button(MESSAGES["btn-club"], "positive", '{"id": "club", "tag": "' + tag + '"}')
        send_msg(msg, keyboard.get_body())
    
def task():
    global _time
    global time
    global life
    
    while life:
        if ntime() - time >= 60*5:
            club = Club(WIDGET["club_tag"].replace("#", "%"))
            rate = 1
            widget = {
                "title": WIDGET["title"],
                "title_url": "https://vk.com/kronos_bs",
                "title_counter": "1",
                "more": "Перейти к полному списку",
                "more_url": "https://vk.com/topic-187742365_41459579",
                "head": [{
                    "text": "Игрок",
                    "align": "left"
                }, {
                    "text": "Трофеи",
                    "align": "right"
                }],
                "body": []
            }
            
            for member in club.get("members"):
                if rate > 10:
                    break
                widget["body"].append([{
                    "text": str(member["name"])
                }, {
                    "text": WIDGET["member"].replace("%trophies%", str(member["trophies"]))
                }])
                rate += 1
              
            widget["title_counter"] = str(rate - 1)
            utils.method("appWidgets.update", {
                "access_token": WIDGET["token"],
                "type": "table",
                "code": "return " + dumps(widget,  ensure_ascii=False, separators=(",", ":")) + ";"
            })
            
            time = ntime()
            
        if ntime() - _time >= 60*60: 
            club = Club(WIDGET["club_tag"].replace("#", "%"))
            members = club.get("members")
            msg =  "Список участников [" + str(len(members)) + "/100]\n"
            mc = 1  
            
            for member in members:
                mmsg = MESSAGES["member"] 
                mmsg = mmsg.replace("%c%", str(mc)) 
                mmsg = mmsg.replace("%role%", getRole(member["role"]))
                mmsg = mmsg.replace("%tag%", member["tag"]) 
                mmsg = mmsg.replace("%name%", member["name"])
                mmsg = mmsg.replace("%trophies%", str(member["trophies"]))
                    
                msg += mmsg + "\n"
                mc += 1 
            
            utils.method("board.editComment", {
                "access_token": DEV_TOKEN,
                "group_id": TOPIC["group-id"],
                "comment_id": TOPIC["comment-id"],
                "topic_id": TOPIC["id"],
                "message": msg
            })
            
            _time = ntime()
        
def handler(event, obj):
    global life
    global peer
    
    if event == "message_new":
        peer = obj["peer_id"]
        user = obj["from_id"]
        text = obj["text"]
        args = text.split( )
        try:
            cmd = args.pop(0)
        except IndexError:
            cmd = text
        user_info = utils.get_user(user) 
        
        if "payload" in obj:
            json = loads(obj["payload"])
            try:
                tag = json["tag"]
                id = json["id"]
            except KeyError:
                tag = ""
                id = ""
            
            if id == "player":
                pl = Player(tag.replace("#","%"))
                brawlers = pl.get("brawlers")
                msg = MESSAGES["id-player"].replace("%name%", str(pl.get("name"))) + " (" + str(len(brawlers)) + "):\n"
                bc = 1
                
                for brawler in brawlers:
                    bmsg = MESSAGES["brawler"]
                    bmsg = bmsg.replace("%c%", str(bc))
                    bmsg = bmsg.replace("%name%", str(brawler["name"]))
                    bmsg = bmsg.replace("%rank%", str(brawler["rank"]))
                    bmsg = bmsg.replace("%power%", str(brawler["power"]))
                    bmsg = bmsg.replace("%trophies%", str(brawler["trophies"]))
                    
                    msg += bmsg + "\n"
                    bc += 1
                send_msg(msg)
               
            elif id == "club":
                cl = Club(tag)
                members = cl.get("members")
                msg = MESSAGES["id-club"].replace("%name%", str(cl.get("name"))) + " (" + str(len(members)) + "):\n"
                mc = 1 
                
                for member in members:
                    mmsg = MESSAGES["member"] 
                    mmsg = mmsg.replace("%c%", str(mc)) 
                    mmsg = mmsg.replace("%role%", getRole(member["role"]))
                    mmsg = mmsg.replace("%tag%", member["tag"]) 
                    mmsg = mmsg.replace("%name%", member["name"])
                    mmsg = mmsg.replace("%trophies%", str(member["trophies"]))
                    
                    msg += mmsg + "\n"
                    mc += 1 
                send_msg(msg)
                
            elif id == "player2":
                getClub(tag.replace("#","%"))
    
        if cmd == "/start":
            send_msg(MESSAGES["start-cmd"].replace("%name%", str(user_info[0]["first_name"])))
            
        elif cmd == "/help" or cmd == "Начать":
            send_msg(MESSAGES["help-cmd"])
            
        elif cmd == "/club":
            try:
                getClub(args[0].replace("#","%"))
            except IndexError:
                send_msg(MESSAGES["args-error"].replace("%args%", "<тег клуба>"))
            
        elif cmd == "/player":
            try:
                player = Player(args[0].replace("#",'%'))
                keyboard = utils.Keyboard(False, True)
                
                if player.get("name") is None:
                    send_msg("Информация о игроке с тегом " + args[0] + " не найдена!")
                else:
                    msg = MESSAGES["player-cmd"]
                    msg = msg.replace("%name%", str(player.get("name")))
                    msg = msg.replace("%tag%", args[0])
                    msg = msg.replace("%trophies%", str(player.get("trophies")))
                    msg = msg.replace("%highestTrophies%", str(player.get("highestTrophies")))
                    msg = msg.replace("%expLevel%", str(player.get("expLevel")))
                    msg = msg.replace("%expPoints%", str(player.get("expPoints")))
                    msg = msg.replace("%3vs3Victories%", str(player.get("3vs3Victories")))
                    msg = msg.replace("%duoVictories%", str(player.get("duoVictories")))
                    msg = msg.replace("%soloVictories%", str(player.get("soloVictories")))
                    
                    if "name" in player.get("club"):
                        msg = msg.replace("%cname%", str(player.get("club")["name"]))
                    else: 
                        msg = msg.replace("%cname%", "None")
                        
                    if "tag" in player.get("club"):
                        msg = msg.replace("%ctag%", str(player.get("club")["tag"]))
                        keyboard.add_button(MESSAGES["btn-player2"], "positive", 
                        '{"id": "player2", "tag": "' + player.get("club")["tag"] + '"}')
                    else:  
                        msg = msg.replace("%ctag%", "None")

                    keyboard.add_button(MESSAGES["btn-player"], "positive", '{"id": "player", "tag": "' + args[0] + '"}')
                    send_msg(msg, keyboard.get_body())
            except IndexError:
                send_msg(MESSAGES["args-error"].replace("%args%", "<тег игрока>"))
                
        elif cmd == "/kill" or cmd == "/stop":
            if isDev(user):
                send_msg(MESSAGES["kill-cmd"])
                life = False
     
thread = Thread(target=task)
thread.start()

while life:
    for event in long_poll.get_events():
        handler(event["type"], event["object"])
else:
    utils.log("отключение..")
    thread.join()