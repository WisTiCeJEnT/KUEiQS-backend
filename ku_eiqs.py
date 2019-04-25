import nontri_authentication
def nontri_login(data):
    username = data["username"]
    password = data["password"]
    if(nontri_authentication.ku_login(username, password)):
        return {"status": "ok", "table": [["01204111", "Compro", "Jui's Room", "24/7"],["    01999111", "kotl", "E201", "09001200"]]}
    else:
        return {"status": "wrong password", "table": [["01204111", "Compro", "Jui's Room", "24/7"],["    01999111", "kotl", "E201", "09001200"]]}
