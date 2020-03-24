from random import randrange

while True:
    x1 = randrange(100)
    x2 = randrange(100)
    y1 = randrange(100)
    y2 = randrange(100)

    s = (y2 - y1) / (x2 - x1)
    if(s < 1.2 and s > 0) :
        pass
    elif(s > -1.2):
        pass
    else:
        print(x1, x2, y1, y2)
        print(s)
        break