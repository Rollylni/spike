from utils import get_role, get_next_level, get_type, get_exp
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotEventType
from supercel import BrawlStars
from vk_api import VkApi
from vkbot import VkBot
from json import dumps, loads
from time import time
from os import getcwd

config = getcwd() + "/config.ini"
logger = getcwd() + "/logger.ini"

bot = VkBot(config, logger)
brawl = BrawlStars("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjJkMTgyZjZmLTU3OWItNDQyMy05MWE4LWQwZTdlMWI5ZjUyZiIsImlhdCI6MTU5Nzg0OTYzMywic3ViIjoiZGV2ZWxvcGVyL2EyNTA1MTMyLTZlMDgtMGVjZS1mZjY3LTU4YmQ4YTA1OWI4MyIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMjEyLjEwOS4xOTcuMTczIl0sInR5cGUiOiJjbGllbnQifV19.xy_T6gDKT8Thzusk_pCg7fUsAR5TvDCI09-F-UyK9RTTm5q6JyOB_iumdqQ6gEvZ-Pektdeus_VFpvWQ1Op0jg")

@bot.event(VkBotEventType.MESSAGE_NEW)
def payload_handler(obj):
    if "payload" in obj:
        data = loads(obj.payload)
        user = bot.get_object(obj.from_id)
        chat = bot.get_chat(obj.peer_id)
        
        if "action" in data and "tag" in data:
            action = data["action"]
            tag = data["tag"]
            if action == "club":
                bot.cmd.commands["club"].exec(user, chat, [tag], obj)
            elif action == "members":
                club = brawl.get_club(tag)
                members= club.get("members")
                msg = "{} {} [{}/100]\n".format(bot.get_messages("btn-club"), club.get("name"), len(members))
                for k in range(0, len(members)):
                    msg += bot.get_messages("member",
                        role=get_role(members[k]["role"]),
                        t=members[k]["trophies"],
                        name=members[k]["name"],
                        tag=members[k]["tag"],
                        n=k+1
                        )
                    msg += "\n"
                chat.sendMessage(msg)
            elif action == "brawlers":
                player = brawl.get_player(tag)
                brawlers = player.get("brawlers")
                msg = "{} {} ({}):\n".format(bot.get_messages("btn-player"), player.get("name"), len(brawlers))
                for k in range(0, len(brawlers)):
                    msg += bot.get_messages("brawler",
                        trophies=brawlers[k]["trophies"],
                        power=brawlers[k]["power"],
                        name=brawlers[k]["name"],
                        rank=brawlers[k]["rank"],
                        n=k+1
                        )
                    msg += "\n"
                chat.sendMessage(msg)
        elif "command" in data and data["command"] == "start":
            chat.sendMessage("{}, привет!".format(user.getName(True)))
            bot.cmd.commands["help"].exec(user, chat, [], obj)
        
@bot.command("help", description="- Список команд")
def help(user, chat, args, obj):
    cmds = bot.cmd.get_commands()
    msg = "Список команд ({}):\n".format(len(cmds))
    for name, cmd in cmds.items():
        msg += "{}{} {}\n".format(bot.prefix[:1], name, cmd.description)
    msg += " \n❗ команды пишутся через {}".format(bot.prefix[:1])
    chat.sendMessage(msg)
    
@bot.command("club", usage="Введите тег клуба!", description="<тег клуба> - Информация о клубе")
def club(user, chat, args, obj):
    club = brawl.get_club(args[0])
    if not club.get("name"):
        sender.sendMessage("Информация о клубе с тегом {} не найдена!".format(args[0]))
        return
        
    msg = bot.get_messages("club", n="\n",
        name=club.get("name"),
        tag=args[0],
        requiredTrophies=club.get("requiredTrophies"),
        trophies=club.get("trophies"),
        members=len(club.get("members")),
        description=club.get("description"),
        type=get_type(club.get("type"))
        )
    kb = VkKeyboard(inline=True)
    kb.add_button(bot.get_messages("btn-club"), color=VkKeyboardColor.NEGATIVE, payload={
        "action": "members",
        "tag": args[0]
    })
    chat.sendKeyboard(msg, kb.get_keyboard())
    
@bot.command("player", usage="Введите тег игрока!", description="<тег игрока> - Информация о игроке")
def player(user, chat, args, obj):
    player = brawl.get_player(args[0])
    name = player.get("name")
    kb = VkKeyboard(inline=True)
    if not name:
        chat.sendMessage("Информация о игроке с тегом {} не найдена!".format(args[0]))
        return
        
    if not player.get("club.tag"):
        club = "Не в клубе"
    else: 
        club = "{} ({})".format(player.get("club.name"), player.get("club.tag"))
        kb.add_button(bot.get_messages("btn-player2"), color=VkKeyboardColor.POSITIVE, payload={
            "action": "club",
            "tag": player.get("club.tag")
        })
            
    msg = bot.get_messages("player", n="\n",
        name=name,
        tag=args[0],
        club=club,
        expLevel=player.get("expLevel"),
        nextExp=get_next_level(player.get("expLevel")),
        expPoints=get_exp(player.get("expPoints"), player.get("expLevel")),
        trophies=player.get("trophies"),
        highestTrophies=player.get("highestTrophies"),
        soloVictories=player.get("soloVictories"),
        duoVictories=player.get("duoVictories"),
        v3vs3Victories=player.get("3vs3Victories")
        )
    kb.add_button(bot.get_messages("btn-player"), color=VkKeyboardColor.POSITIVE, payload={
        "action": "brawlers",
        "tag": args[0]
    })
    chat.sendKeyboard(msg, kb.get_keyboard())

@bot.command("info", description="- Информация о боте")
def info(user, chat, args, obj):
    do = round(time() - obj["date"])
    chat.sendMessage(bot.get_messages("info_cmd",
        prefix=bot.prefix,
        lang=bot.lang,
        tasks=len(bot.tasks.tasks),
        cmds=len(bot.cmd.commands),
        ut=bot.uptime(),
        do=do
        ))
    
@bot.task(3600*12, True)
def set_topic():
    user = VkApi(token=bot.get_settings("admin_token"), api_version=bot.vk.api_version)
    members = brawl.get_club_members("#R020J99L").response["items"]
    msg = "Список участников [{}/100]\n".format(len(members))
    for k in range(0, len(members)):
        msg += bot.get_messages("member",
            role=get_role(members[k]["role"]),
            t=members[k]["trophies"],
            name=members[k]["name"],
            tag=members[k]["tag"],
            n=k+1
            )
        msg += "\n"
        
    try:
        user.method("board.editComment", {
            "group_id": bot.lp.group_id,
            "comment_id": 2,
            "topic_id": 41459579,
            "message": msg
            })
    except:
        bot.log_exception()
    
@bot.task(180, True)
def set_widget():
    service = VkApi(token=bot.get_settings("service_token"), api_version=bot.vk.api_version)
    widget = {
        "title": "Список лучших игроков клана",
        "title_url": "https://vk.com/kronos_bs",
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
    members = brawl.get_club_members("#R020J99L", limit=11).response["items"]
    for k in range(0, len(members)):
        widget["body"].append([{
            "text": "{}. {}".format(k+1, members[k]["name"])
        }, {
            "text": bot.get_messages("widget_member", t=members[k]["trophies"])
        }])
    widget["title_counter"] = len(members)
    
    try:
        service.method("appWidgets.update", {
            "type": "table",
            "code": "return " + dumps(widget,  ensure_ascii=False, separators=(",", ":")) + ";"
        })
    except:
        bot.log_exception()
        
if __name__ == "__main__":
    bot.start()