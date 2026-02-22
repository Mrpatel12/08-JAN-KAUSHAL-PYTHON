f1 = open("python.txt","r")

print(f1.read())
print(f1.readlines())
print(f1.readline())

for i in f1:
    print(i)