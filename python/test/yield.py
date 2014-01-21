def createGenerator():
    mylist = range(3)
    for i in mylist:
        if i > 0:
            i = i+1
        yield i*i

mygenerator = createGenerator()
for i in mygenerator:
    print(i)
