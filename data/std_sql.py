import json
f = open("data.json")
data = eval(f.read())
f.close()
#print(data)
f = open("stdEnroll_sql.txt", 'w')
for std_id in data.keys():
    #print(std_id)
    for course in data[std_id]:
        #print(course)
        c = course
        if(c[1]!='0'):
            f.write(f"({std_id}, '{c[0]}', {c[1]}, 2561, 1),\n")
            print(f"({std_id}, '{c[0]}', {c[1]}, 2561, 1),")
        if(c[2]!='0'):
            f.write(f"({std_id}, '{c[0]}', {c[2]}, 2561, 1),\n")
            print(f"({std_id}, '{c[0]}', {c[2]}, 2561, 1),")
f.close()
