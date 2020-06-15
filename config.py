# vk api
TOKEN = ""
VERSION = "5.103"
LANG = "ru"

# Bot
BS_API_KEY = ""
DEV_TOKEN = ""
DEV_IDS = []
GROUP_ID = ""
WAIT = 25

MESSAGES = {
    "perm-denied": "У вас недостаточно прав.",
    "cmd-not-found": "Я вас не понял, введите /help",
    "args-error": "Пожалуйста укажите аргументы: %args%",
    "kill-cmd": "Бот успешно отключен✅",
    "start-cmd": "Привет %name%\nЧтобы узнать мои команды введите /help",
    "btn-player": "📈 Бойцы игрока",
    "btn-player2": "🛡 Клан игрока",
    "btn-club": "👥 Участники клуба",
    "id-club": "🛡 участники клуба %name%",
    "member": "%c%. %name%(%tag%) %trophies%🏆 [%role%]",
    "id-player": "📈Бойцы игрока %name%",
    "brawler": "%c%. %name% ранг %rank% (%trophies%🏆) ур. %power%🔰",
    "help-cmd": "🗒Список моих команд:\n" +
                "- player <тег игрока>: информация о игроке\n" +
                "- club <тег клуба>: информация о клубе\n" +
                " \n❗Команды пишутся через слэш(/)",
                
    "club-def": "🔍Информация о клубе:\n" +
                "🛡название: %name% (%tag%)\n" +
                "🔥нужно трофеев: %requiredTrophies%\n" +
                "👥участники: %members%/100\n" +
                "🏆трофеи: %trophies%\n" +
                "♨️тип: %type%\n" +
                " \n📌Описание: %description%",
                
    "player-cmd": "🔍Информация о игроке:\n" +
                  "👤никнейм: %name% (%tag%)\n" +
                  "🔰уровень: %expLevel% [EXP: %expPoints%]\n" +
                  "🛡клуб: %cname% (%ctag%)\n" +
                  "🏆трофеи: %trophies%\n" +
                  "🔝лучшие трофеи: %highestTrophies%\n" +
                  "🗡победы: %soloVictories%\n" +
                  "👥парные победы: %duoVictories%\n" +
                  "🥉победы 3vs3: %3vs3Victories%\n"
}

TOPIC = {
    "comment-id": "",
    "group-id": "",
    "id": ""
}

WIDGET = {
    "token": "",
    "club_tag": "",
    "title": "Список лучших игроков",
    "member": "%trophies%🏆"
}
