file_name = input("filename: ")
f = open(file_name)
l = f.read().split('\n')
f.close()
f = open(file_name.split('.')[0]+"_sql.txt", 'w')
print("INSERT INTO examtbl(date, time, courseid, sec, room, startid, endid, year, sem, mf) VALUES\n")
f.write("INSERT INTO examtbl(date, time, courseid, sec, room, startid, endid, year, sem, mf) VALUES\n")
for i in range(len(l)):
    l[i] = l[i].split(',')
ll = l[-1]
l = l[:-1]
for i in l:
    print(f"('{i[0]}', '{i[1]}', '{i[2]}', {i[3]}, '{i[4]}', {i[5]}, {i[6]}, {i[7]}, {i[8]}, '{i[9]}'),")
    f.write(f"('{i[0]}', '{i[1]}', '{i[2]}', {i[3]}, '{i[4]}', {i[5]}, {i[6]}, {i[7]}, {i[8]}, '{i[9]}'),\n")
print(f"('{ll[0]}', '{ll[1]}', '{ll[2]}', {ll[3]}, '{ll[4]}', {ll[5]}, {ll[6]}, {ll[7]}, {ll[8]}, '{ll[9]}');")
f.write(f"('{ll[0]}', '{ll[1]}', '{ll[2]}', {ll[3]}, '{ll[4]}', {ll[5]}, {ll[6]}, {ll[7]}, {ll[8]}, '{ll[9]}');")
f.close()
