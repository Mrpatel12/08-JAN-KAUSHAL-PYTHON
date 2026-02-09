data ={}

n = int(input("Enter number of items:"))

for i in range(n):

 id = input("Enter your id:")
 name = input("Enter your name:")
 Emailid = input("Enter your emailid:")

data.__dir__= [id,name,Emailid]
 
print("data",data)
