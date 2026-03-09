# Q1). Write a Python program to create a list with elements of multiple data types (integers,
# strings, floats, etc.).

# Ans.
my_list = [10, "Hello", 3.14, True, 25, "Python"]

print("List with multiple data types:")
print(my_list)

print("\nAccessing elements:")
print("Integer:", my_list[0])
print("String:", my_list[1])
print("Float:", my_list[2])
print("Boolean:", my_list[3])

# Q2). Write a Python program to access elements at
# different index positions.

# Ans. 
my_list = [10, 20, 30, 40, 50, "Python", 3.14]

print("Element at index 0:", my_list[0])
print("Element at index 2:", my_list[2])
print("Element at index 4:", my_list[4])
print("Element at index 5:", my_list[5])
print("Element at index 6:", my_list[6])

print("Last element:", my_list[-1])
print("Second last element:", my_list[-2])


# Q3). Write a Python program to add elements to a 
# list using insert() and append().

# Ans. 
my_list = []

my_list.append(10)
my_list.append(20)
my_list.append(30)

print("List after using append():", my_list)

my_list.insert(1, 15)   
my_list.insert(3, 25)   

print("List after using insert():", my_list)

# Q4). Write a Python program to remove elements from 
# a list using pop() and remove().

# Ans.
my_list = [10, 20, 30, 40, 50]

print("Original List:", my_list)

my_list.pop() 
print("List after pop():", my_list)

my_list.remove(20)
print("List after remove():", my_list)

# Q5). Write a Python program to iterate over 
# a list using a for loop

# Ans.
my_list = [10, 20, 30, 40, 50]

print("Elements in the list:")

for element in my_list:
    print(element)

# Q6). Write a Python program to sort a list 
# using both sort() and sorted().

# Ans.    

my_list = [50, 20, 40, 10, 30]

print("Original List:", my_list)

my_list.sort()
print("List after using sort():", my_list)

numbers = [60, 25, 15, 45, 35]

sorted_list = sorted(numbers)

print("Original numbers list:", numbers)
print("List after using sorted():", sorted_list)

# Q7). Write a Python program to create a 
# tuple with multiple data types.

# Ans.

my_tuple = (10, "Hello", 3.14, True, "Python")

print("Tuple with multiple data types:")
print(my_tuple)

print("\nAccessing elements:")
print("Integer:", my_tuple[0])
print("String:", my_tuple[1])
print("Float:", my_tuple[2])
print("Boolean:", my_tuple[3])

# Q8). Write a Python program to concatenate two tuples.

# Ans.
tuple1 = (1, 2, 3)
tuple2 = ("A", "B", "C")

result = tuple1 + tuple2

print("Tuple 1:", tuple1)
print("Tuple 2:", tuple2)
print("Concatenated Tuple:", result)

# Q9). Write a Python program to access values
# between index 1 and 5 in a tuple.

# Ans.
my_tuple = (10, 20, 30, 40, 50, 60, 70)

result = my_tuple[1:5]

print("Original Tuple:", my_tuple)
print("Values between index 1 and 5:", result)

# Q10). Write a Python program to access alternate values 
# between index 1 and 5 in a tuple.

# Ans.
my_tuple = (10, 20, 30, 40, 50, 60, 70)

result = my_tuple[1:6:2]

print("Original Tuple:", my_tuple)
print("Alternate values between index 1 and 5:", result)

# Q11). Write a Python program to create a dictionary 
# with 6 key-value pairs.

# Ans. 
student = {
    "id": 101,
    "name": "Rahul",
    "age": 21,
    "course": "Python",
    "city": "Vadodara",
    "marks": 85
}

print("Student Dictionary:")
print(student)

# Q12). Write a Python program to access values using 
# dictionary keys.

# Ans.
student = {
    "id": 101,
    "name": "kaushal",
    "age": 22,
    "course": "Python",
    "city": "Jamnagar",
    "marks": 78
}
print("Student ID:", student["id"])
print("Student Name:", student["name"])
print("Student Age:", student["age"])
print("Course:", student["course"])
print("City:", student["city"])
print("Marks:", student["marks"])

# Q13). Write a Python program to update a value in a 
# dictionary

# Ans.
student = {
    "id": 101,
    "name": "kaushal",
    "age": 22,
    "course": "Python",
    "city": "Jamnagar",
    "marks": 78
}

print("Original Dictionary:")
print(student)

student["marks"] = 90

print("\nUpdated Dictionary:")
print(student)

# Q14). Write a Python program to merge two lists into one 
# dictionary using a loop.

# Ans.
keys = ["id", "name", "age", "course"]
values = [101, "kaushal", 22, "Python"]

my_dict = {}

for i in range(len(keys)):
    my_dict[keys[i]] = values[i]

print("Merged Dictionary:")
print(my_dict)

# Q15). Write a Python program to create a function that takes 
# a string as input and prints it.


# Ans.
def print_string(text):
    print("The string is:", text)

user_input = input("Enter a string: ")
print_string(user_input)

# Q16). Write a Python program to create 
# a calculator using functions.

# Ans.
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

print("Choose operation:")
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")

choice = input("Enter choice (1/2/3/4): ")

if choice == "1":
    print("Result:", add(num1, num2))

elif choice == "2":
    print("Result:", subtract(num1, num2))

elif choice == "3":
    print("Result:", multiply(num1, num2))

elif choice == "4":
    print("Result:", divide(num1, num2))

else:
    print("Invalid choice")

# Q17). Write a Python program to import the math module 
# and use functions like sqrt(), ceil(),floor().

# Ans.
import math

num = 25
num2 = 4.7

print("Square root of", num, "is:", math.sqrt(num))
print("Ceil value of", num2, "is:", math.ceil(num2))
print("Floor value of", num2, "is:", math.floor(num2))

# Q18). Write a Python program to generate random numbers 
# using the random module.

# Ans.
import random

rand_int = random.randint(1, 100)
print("Random Integer:", rand_int)

rand_float = random.random()
print("Random Float:", rand_float)

numbers = [10, 20, 30, 40, 50]
rand_choice = random.choice(numbers)
print("Random Choice from list:", rand_choice)



