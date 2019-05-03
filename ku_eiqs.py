import nontri_authentication
import postgresql_api
import dateconverter
import json
import os
import random
import time

demo_user = eval(os.environ["DEMO_USER"])
admin_token = {}
std_token = {}

def check_token(uid, u_token):
    if(uid[0].lower() == 'b'):
        if(uid not in std_token):
            return 0
        elif(std_token[uid] != u_token):
            return 0
    else:
        if(uid not in admin_token):
            return 0
        elif(admin_token[uid] != u_token):
            return 0
    return 1

def gen_token(uid):
    #random.seed(time.ctime())
    new_token = str(random.randint(1000000000,9999999999))
    global std_token
    global admin_token
    group = ''
    if(uid[0].lower() == 'b'):
        std_token[uid] = new_token
        group = 's'
    else:
        admin_token[uid] = new_token
        group = 'l'
    return [new_token, group]

def get_user_data(uid):
    query_string = f"""SELECT stdid, stdfname, stdlname, stddata.email, depname, facname, advisorid
FROM stddata, faculty, department
WHERE stddata.depid=department.depid
AND department.facid=faculty.facid

AND stddata.stdid={uid[1:]}"""
    res = postgresql_api.get_data(query_string)
    print(res)
    data = {
        "stdid": res[0],
        #"name": res[1] + ' ' + res[2],
        #"email": res[3],
        #"department": res[4],
        #"faculty": res[5],
        #"advisorid": res[6]
    }
    return res

def nontri_login(data):
    username = data["username"]
    password = data["password"]
    if(username in demo_user):
        if(demo_user[username] == password):
            token = gen_token(username)
            group = token[1]
            token = token[0]
            return {
            "status": "ok", 
            "token": token, 
            "group": group, 
            "userdata": {"name": username}
            }
    elif(nontri_authentication.ku_login(username, password)):
        token = gen_token(username)
        group = token[1]
        token = token[0]
        return {
        "status": "ok", 
        "token": token, 
        "group": group,
        "userdata": get_user_data(username)
        }
    return {"status": "wrong password", "token": ""}

def query_data(data):
    username = data["username"]
    u_token = data["token"]
    query_string = data["query_string"]#for temporary use only
    if(not check_token(username, u_token)):
        return {"status": "wrong token", "data": []}
    res = postgresql_api.get_data(query_string)
    return{"status": "ok", "data": str(res)}
    
def exam_tbl(data):
    ans = []
    res = {}
    tbl = data["tbl"]
    course = f"(examtbl.courseid='{tbl[0]['key']}' AND examtbl.sec={int(tbl[0]['sec'])})"
    for i in range(1,len(tbl)):
        int(tbl[i]['key'])  #Try to error
        int(tbl[i]['sec'])  #Try to error too
        course += f" OR (examtbl.courseid='{tbl[i]['key']}' AND examtbl.sec={int(tbl[i]['sec'])})"
    query_string = """
    SELECT course.courseid, coursename, sec, date, time, room FROM examtbl, course
    WHERE examtbl.courseid=course.courseid
    AND ("""+course+") AND mf='f' AND year=2561 AND sem=2"
    #print(query_string)
    exam = postgresql_api.get_data(query_string)
    #print("print",exam)
    for i in exam:
        res[i[0]] = {"key": i[0], #courseid
        "coursename": i[1],
        "sec": str(i[2]),
        "date": dateconverter.dateconverter(i[3]),
        "caldate": f"{int(i[3][4:8])-543}-{i[3][2:4]}-{i[3][0:2]}",
        "time": f"{i[4][0:2]}:{i[4][2:4]} - {i[4][4:6]}:{i[4][6:8]}",
        "room": i[5]
        }
    for i in range(len(tbl)):
        if(tbl[i]['key'] in res.keys()):
            ans.append(res[tbl[i]['key']])
    return(ans)
    
#SELECT course.courseid, coursename, sec, date, time, room FROM examtbl, course
#WHERE examtbl.courseid=course.courseid
#AND ((examtbl.courseid='01204351' AND examtbl.sec=1) OR (examtbl.courseid='01204225' AND examtbl.sec=1))



