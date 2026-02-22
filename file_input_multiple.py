fl =open("python4.txt","w")

n = int(input("Enter number of Students:"))

for i in range(n):
    name = input("Enter name of student:")
    rollno = input("Enter roll numbers of student:")

    fl.write(name+" "+rollno+"\n")
fl.close()