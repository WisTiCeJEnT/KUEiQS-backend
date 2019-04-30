def dateconverter(x):
    date=x[0:2]
    month=int(x[2:4])-1
    year=int(x[4:8])
    monthans = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    return (date[0]+date[1]+' '+monthans[month]+' '+str(year-543))
