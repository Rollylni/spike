#детерминированные функции

def get_next_level(level):
    return 30 + 10 * int(level)

def get_exp(exp, level):
    for l in range(1, level):
        exp -= get_next_level(l)
    return exp

def get_type(type):
    if type == "open":
        return "открытый"
    elif type == "closed":
        return "закрытый"
    else:
        return "по-приглашению"#

def get_role(role):
    if role == "president":
        return "Президент"
    elif role == "vicePresident":
        return "Вице-президент"
    elif role == "senior":
        return "Ветеран"
    else:
        return "Участник"