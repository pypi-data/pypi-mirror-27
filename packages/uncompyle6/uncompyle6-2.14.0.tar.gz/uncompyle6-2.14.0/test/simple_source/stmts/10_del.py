a = (1, 2, 3)
del a

b = [4, 5, 6]
del b[1]
del b[:]

c = [0,1,2,3,4]
del c[:1]
del c[2:3]

d = [0,1,2,3,4,5,6]
del d[1:3:2]

e = ('a', 'b')
def foo():
    global e
    del e
