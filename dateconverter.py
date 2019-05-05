def dateconverter(x):
    date=x[0:2]
    month=int(x[2:4])-1
    year=int(x[4:8])
    monthans = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    return (date[0]+date[1]+' '+monthans[month]+' '+str(year-543))

def caldate(d):
    return f"{int(d[4:8])-543}-{d[2:4]}-{d[0:2]}"

def timeconverter(t):
    return f"{t[0:2]}:{t[2:4]} - {t[4:6]}:{t[6:8]}"