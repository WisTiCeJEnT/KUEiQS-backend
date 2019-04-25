f = open("dep.csv").read()
l = f.split('\n')
for i in range(len(l)):
    l[i] = l[i].split(',')
for i in l:
    print(f"('{i[0]}', '{i[0][0]}', '{i[1]}'),")