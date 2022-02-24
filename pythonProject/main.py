from decimal import Decimal, getcontext

getcontext().prec = 6
print(float(Decimal(1.1 + 1.2 + 1.3)/Decimal(3)))
print("")
# formatted strings
print("{} can be {}".format("strings", "interpolated"))

print("")
#print("Hello, World", end='!')

print("")
#print(input("Name Please: "))


print("")
a = [1,2,3,4,5]
print(a[1:3]) #shows 2,3
print(a[1:-1]) #shows 2,3,4
print(a[0:-1]) #shows 1,2,3,4
print(a[0:5]) #shows 1,2,3,4,5
print(a[::2]) #shows every second
print(a[::-1]) #reverse order

li2 = a[:] # Making a copy of a || li2 == 'a' is copying ref making '==' and 'is' true
print(li2 == a) # True
print(li2 is a) # False