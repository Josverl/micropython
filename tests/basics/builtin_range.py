# test builtin range type

# print
print(range(4))

# bool
print(bool(range(0)))
print(bool(range(10)))

# len
print(len(range(0)))
print(len(range(4)))
print(len(range(1, 4)))
print(len(range(1, 4, 2)))
print(len(range(1, 4, -1)))
print(len(range(4, 1, -1)))
print(len(range(4, 1, -2)))

# subscr
print(range(4)[0])
print(range(4)[1])
print(range(4)[-1])

# slice
print(range(4)[0:])
print(range(4)[1:])
print(range(4)[1:2])
print(range(4)[1:3])
print(range(4)[1::2])
print(range(4)[1:-2:2])
print(range(1, 4)[:])
print(range(1, 4)[0:])
print(range(1, 4)[1:])
print(range(1, 4)[:-1])
print(range(7, -2, -4)[:])
print(range(1, 100, 5)[5:15:3])
print(range(1, 100, 5)[15:5:-3])
print(range(100, 1, -5)[5:15:3])
print(range(100, 1, -5)[15:5:-3])

# for this case uPy gives a different stop value but the listed elements are still correct
print(list(range(7, -2, -4)[2:-2:]))

# zero step
try:
    range(1, 2, 0)
except ValueError:
    print("ValueError")

# bad unary op
try:
    -range(1)
except TypeError:
    print("TypeError")

# bad subscription (can't store)
try:
    range(1)[0] = 1
except TypeError:
    print("TypeError")

# index method
print(range(5, 50, 5).index(25))  # should print 4

# index method with value not in range
try:
    print(range(5, 50, 5).index(30))
except ValueError:
    print("ValueError")

# index method with empty range
try:
    print(range(0).index(0))
except ValueError:
    print("ValueError")
