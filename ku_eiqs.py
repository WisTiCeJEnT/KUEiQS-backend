import nontri_authentication
import json
import os
import random
import time

demo_user = eval(os.environ["DEMO_USER"])
token = {}

def check_token(uid, u_token):
    if(uid not in token):
        return 0
    elif(token[uid] != u_token):
        return 0
    return 1

def gen_token(uid):
    random.seed(time.ctime())
    new_token = random.randint(1000000,9999999)
    global token
    token[uid] = new_token
    return str(new_token)

def nontri_login(data):
    username = data["username"]
    password = data["password"]
    if(username in demo_user):
        if(demo_user[username] == password):
            return {"status": "ok", "token": gen_token(username)}
    elif(nontri_authentication.ku_login(username, password)):
        return {"status": "ok", "token": gen_token(username)}
    return {"status": "wrong password", "token": ""}
