s1 = int(input("Enter Marks of Sub 1:"))
s2 = int(input("Enter Marks of Sub 2:"))
s3 = int(input("Enter Marks of Sub 3:"))
s4 = int(input("Enter Marks of Sub 4:"))

s1>=40 and s2>=40 and s3>=40 and s4>=40

total=s1+s2+s3+s4
percentage=(total/400)*100

print("total Marks:",total)
print("percentage:",percentage)

print("Grade:",Grade)

if percentage>=80:
    print("Your garde is A")

elif percentage>=65:
    print("Your grade is B ")

elif percentage>=50:
    print("Your grade is C:")

elif percentage>=40:
    print("Your Grade is F:")



