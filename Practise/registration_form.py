First_name = input("Enter Your First Name:")
Last_name = input("Enter Your Last Name:")
email = input("Enter Your Email ID:")
Mobile_number = input("Enter Your Mobile Number:")
Password = input("Enter Your Password:")
Confirm_Password = input("Enter Your Confirm Password")


print("First Name:",chr)

First_name.isalpha()

if First_name.isalpha():

    print("Your Name is Valid")
else:
    print("Your Name is not Valid")

print("Last Name:",chr)



Last_name.isalpha()

if Last_name.isalpha():

    print("Your Name is Valid")
else:
    print("Your Name is not Valid")



print("Email ID:",email)

if email.lower():
    
 print("Your Email ID is Valid")

else:
 print("Your Email ID is not Valid")



Mobile_number.isdigit()

if Mobile_number.isdigit() and len(Mobile_number)==10:
   print("Your Mobile Number is Valid")
else:
   print("Your Mobile Number is not Valid")



print("Password:",Password)

if len(Password)>=8 and len(Password)<=12:
      
      print("Your Password is Valid:")
else:
      print("Your Password is not Valid:")



print("Confirm-Password:",Confirm_Password)

if Confirm_Password==Password:
    
      print("Your Password is Valid:")
else:
      print("Your Password is not Valid:")




      