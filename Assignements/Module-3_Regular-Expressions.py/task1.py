import re

# mysting = "Sanket2020"
# x = re.search("^",mysting)

mystring = "Kaushal120804@gmail.com"

pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

if re.match(pattern,mystring):
    print("Valid Email")
else:
    print("Invalid Email")