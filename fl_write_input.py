fl = open("python.txt","w")

stdid = input("Enter student id:")
stdname = input("Enter student name:")

fl.write(f"student id:{stdid}\nstudent name:{stdname}")