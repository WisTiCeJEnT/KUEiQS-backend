import nontri_authentication
import postgresql_api
import dateconverter
import json
import os
import random
import time

STD_QUERY_LIST = ['stdenroll.sem', 'examtbl.mf', 'examtbl.year']
ADMIN_QUERY_LIST = ['stddata.stdid', 'stddata.stdfname', 'stddata.stdlname', 'course.courseid', 'stdenroll.sec', 'examtbl.sem', 'examtbl.mf', 'examtbl.date', 'examtbl.time', 'examtbl.year']
demo_user = eval(os.environ["DEMO_USER"])
admin_token = {}
std_token = {}

def check_token(data):
    try:
        uid = data["username"]
        u_token = data["token"]
    except:
        return 0
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
    #print(res)
    res = res[0]
    data = {
        "stdid": res[0],
        "name": res[1] + ' ' + res[2],
        "email": res[3],
        "department": res[4],
        "faculty": res[5],
        "advisorid": res[6]
    }
    return data

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
            "userdata": {"name": username}, 
            "authentication": True
            }
    elif(nontri_authentication.ku_login(username, password)):
        token = gen_token(username)
        group = token[1]
        token = token[0]
        return {
        "status": "ok", 
        "token": token, 
        "group": group,
        "userdata": get_user_data(username), 
        "authentication": True
        }
    return {"status": "wrong password", "token": "", "authentication": False}

def query_data(data):
    query_string = data["query_string"]#for temporary use only
    if(not check_token(data)):
        return {"status": "wrong token", "data": []}
    res = postgresql_api.get_data(query_string)
    return{"status": "ok", "data": str(res)}
    
def exam_tbl(data):
    res = {}
    tbl = data["tbl"]
    int(tbl[0]['key'])
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
        res[i[3]+i[4]] = {"key": i[0], #courseid
        "coursename": i[1],
        "sec": str(i[2]),
        "date": dateconverter.dateconverter(i[3]),
        "caldate": dateconverter.caldate(i[3]),
        "time": dateconverter.timeconverter(i[4]),
        "room": i[5]
        }
    return(sort_by_date(res))
        
def sort_by_date(exam_dict):
    new_exam = {}
    for k in exam_dict.keys():
        new_key = k[4:6]+k[2:4]+k[0:2]+k[6:]
        new_exam[new_key] = exam_dict[k]
    sorted_list = sorted(new_exam.keys())
    res = []
    for i in sorted_list:
        res.append(new_exam[i])
    return res

def type_query(this_query):
    if(type(this_query) == type(ADMIN_QUERY_LIST[0])):
        this_query = "'"+this_query+"'"
    else:
        this_query = int(this_query)
    return this_query

def stdQuery(data):
    if(check_token(data)):
        stdquery_data = data['query_data']
        query_string = """SELECT course.courseid, course.coursename, stdenroll.sec, examtbl.date, examtbl.time, examtbl.room
FROM examtbl, course, stdenroll
WHERE examtbl.courseid=course.courseid
AND stdenroll.courseid=course.courseid
AND stdenroll.sec=examtbl.sec
AND stdenroll.sem=examtbl.sem
AND stdenroll.year=examtbl.year
AND stdenroll.stdid BETWEEN startid AND endid 

AND stdenroll.stdid="""+f"{int(data['username'][1:])} "
        for i in STD_QUERY_LIST:
            short_i = i[i.find('.')+1:]
            if short_i in stdquery_data:
                query_string += f"AND {i}={type_query(stdquery_data[short_i])} " 
        #print(query_string)
        exam = postgresql_api.get_data(query_string)
        res = {}
        for i in exam:
            res[i[3]+i[4]] = {"key": i[0], #courseid
            "coursename": i[1],
            "sec": str(i[2]),
            "date": dateconverter.dateconverter(i[3]),
            "caldate": dateconverter.caldate(i[3]),
            "time": dateconverter.timeconverter(i[4]),
            "room": i[5]
            }
        return(sort_by_date(res))
    else:
        return {"status": "wrong token"}

def adminQuery(data):
    if(check_token(data)):
        adminquery_data = data['query_data']
        query_string = """SELECT course.courseid, course.coursename, stdenroll.sec, examtbl.date, examtbl.time, examtbl.room
FROM examtbl, course, stddata, stdenroll, faculty, department, lecdata
WHERE examtbl.courseid=course.courseid
AND stddata.advisorid=lecdata.lecid
AND stddata.stdid=stdenroll.stdid
AND stddata.depid=department.depid
AND department.facid=faculty.facid
AND stdenroll.courseid=course.courseid
AND stdenroll.sec=examtbl.sec
AND stdenroll.sem=examtbl.sem
AND stdenroll.year=examtbl.year
AND stddata.stdid BETWEEN startid AND endid

"""
        for i in ADMIN_QUERY_LIST:
            short_i = i[i.find('.')+1:]
            if short_i in adminquery_data:
                
                query_string += f"AND {i}={type_query(adminquery_data[short_i])} " 
        #print(query_string)
        exam = postgresql_api.get_data(query_string)
        res = {}
        for i in exam:
            res[i[3]+i[4]] = {"key": i[0], #courseid
            "coursename": i[1],
            "sec": str(i[2]),
            "date": dateconverter.dateconverter(i[3]),
            "caldate": dateconverter.caldate(i[3]),
            "time": dateconverter.timeconverter(i[4]),
            "room": i[5]
            }
        return(sort_by_date(res))
    else:
        return {"status": "wrong token"}

#SELECT course.courseid, coursename, sec, date, time, room FROM examtbl, course
#WHERE examtbl.courseid=course.courseid
#AND ((examtbl.courseid='01204351' AND examtbl.sec=1) OR (examtbl.courseid='01204225' AND examtbl.sec=1))



