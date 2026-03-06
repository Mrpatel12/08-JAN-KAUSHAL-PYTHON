class studentinfo():
    def __init__(self,id,name,city):
        self.id = id
        self.name = name
        self.city = city

stdata = []        

for i in range(1):
    id = input("Enter your ID:")
    name = input("Enter your name:")
    city = input ("Enter your city:")

    st = studentinfo(id,name,city)
    stdata.append(st)

for i in stdata:
     print(i.id)
     print(i.name)
     print(i.city)

