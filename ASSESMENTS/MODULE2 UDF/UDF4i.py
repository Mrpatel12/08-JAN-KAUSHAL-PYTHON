# UDF enter your id name city and store in the list
# and print output in list



def getdata(data_list): 
     user_id = input("Enter your ID:")
     user_name = input("Enter your name:")
     user_city = input("Enter your city:")

     data_list 
     {
          "ID": user_id,
          "Name":user_name,
          "City":user_city

     }

     data_list.append(data_list)
     print("Your data stored successfully.")

     data_list = []

     while True:

        getdata(data_list)
        other_user = input("If you want to add another" \
                           "user (Yes/No)")
        
        if other_user != 'Yes':
            break

        print ("\n Whole record ----")
        for user in data_list:
          print(user)

