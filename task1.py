# timestamp current time&date
# id(auto generated)
# name
# city

import datetime

datetime =datetime.datetime.now()
A = print(datetime)

fl =open("python1.txt","w")
 
import uuid

id = uuid.uuid1()

name = input("Enter your name:")
city = input("Enter your city:")

fl.write("Timestamp:"+str(datetime)+"\n")
fl.write("id:"+str(id)+"\n")
fl.write("name:"+str(name)+"\n")
fl.write("city:"+str(city)+"\n")
fl.close()




