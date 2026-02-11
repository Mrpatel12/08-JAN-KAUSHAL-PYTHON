my_string = "Python String Slicing"

print(f"Original string: '{my_string}'\n")

slice1 = my_string[:6]
print(f"From start to index 6: '{slice1}'") 

slice2 = my_string[7:]
print(f"From index 7 to end: '{slice2}'")

slice3 = my_string[7:14]
print(f"From index 7 to 14: '{slice3}'") 

slice4 = my_string[:]
print(f"Entire string: '{slice4}'") 

slice5 = my_string[::2]
print(f"Every second character: '{slice5}'")

slice6 = my_string[0:15:3]
print(f"Every third character (0-14): '{slice6}'")

slice7 = my_string[-7:-1]
print(f"Using negative indices (-7 to -1): '{slice7}'") 

slice8 = my_string[-5:]
print(f"Last 5 characters: '{slice8}'") 

slice9 = my_string[::-1]
print(f"Reversed string: '{slice9}'") 