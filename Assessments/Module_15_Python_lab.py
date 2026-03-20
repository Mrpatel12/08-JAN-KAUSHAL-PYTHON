# Q1). Write a Python program to print a formatted string using print() and f-string.
# Ans.

name = "Kaushal"
age = 22
city = "Jamnagar"

print("My name is", name, "I am", age, "years old and I live in", city)
print(f"My name is {name}, I am {age} years old and I live in {city}.")

# Q2). Write a Python program to read a name and age from the user and print a formatted output.
# Ans.

name = input("Enter your name: ")
age = int(input("Enter your age: "))
print(f"Hello {name}, you are {age} years old.")

# Q3). Write a Python program to open a file in write mode, write some text, and then close it.
# Ans.

file = open("sample.txt", "w")
file.write("Hello, this is my first file in Python.\n")
file.write("Writing data using file handling.")

file.close()
print("Data written to file successfully.")

# Q4). Write a Python program to read the contents of a file and print them on the console.
# Ans.

file = open("sample.txt", "r")
content = file.read()
print(content)
file.close()

# Q5). Write a Python program to write multiple strings into a file.
# Ans.

lines = [
    "Hello, this is line 1.\n",
    "This is line 2.\n",
    "Python file handling is easy!\n"
]

with open("sample.txt", "w") as file:
    file.writelines(lines)

print("Multiple lines written successfully.")

# Q6). Write a Python program to handle exceptions in a simple calculator (division by zero, invalid
# input).
# Ans.

try:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    operator = input("Enter operator (+, -, *, /): ")

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        result = num1 / num2   
    else:
        print("Invalid operator!")
        result = None

    if result is not None:
        print(f"Result: {result}")

except ValueError:
    print("Error: Please enter valid numbers.")

except ZeroDivisionError:
    print("Error: Cannot divide by zero.")

except Exception as e:
    print("An unexpected error occurred:", e)

# Q7). Write a Python program to demonstrate handling multiple exceptions.
# Ans.

try:

    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))

    result = num1 / num2
    my_list = [10, 20, 30]
    index = int(input("Enter index (0-2): "))
    print("Element:", my_list[index])

    print("Result:", result)

except ValueError:
    print("Error: Please enter valid integers.")

except ZeroDivisionError:
    print("Error: Cannot divide by zero.")

except IndexError:
    print("Error: List index out of range.")

except Exception as e:
    print("Unexpected error:", e)

finally:
    print("Program execution completed.")

# Q8). Write a Python program to create a class and access its properties using an object.
# Ans.

class Person:
    def __init__(self, name, age):
        self.name = name      
        self.age = age        

p1 = Person("Kaushal", 22)
print("Name:", p1.name)
print("Age:", p1.age)

# Q9). Write Python programs to demonstrate different types of inheritance (single, multiple,
# multilevel, etc.).
# Ans.

# 1. Single Inheritance

class Parent:
    def show(self):
        print("This is Parent class")

class Child(Parent):
    def display(self):
        print("This is Child class")

obj = Child()
obj.show()     
obj.display()

# 2. Multiple Inheritance

class Father:
    def skill1(self):
        print("Father: Gardening")

class Mother:
    def skill2(self):
        print("Mother: Cooking")

class Child(Father, Mother):
    def skill3(self):
        print("Child: Playing")

obj = Child()
obj.skill1()
obj.skill2()
obj.skill3()

# 3. Multilevel Inheritance

class Grandparent:
    def house(self):
        print("Grandparent's House")

class Parent(Grandparent):
    def car(self):
        print("Parent's Car")

class Child(Parent):
    def bike(self):
        print("Child's Bike")

obj = Child()
obj.house()
obj.car()
obj.bike()

# Q10). Write Python programs to demonstrate method overloading and method overriding.
# Ans.

# 1. Method Overloading
class Calculator:
    def add(self, a, b=0, c=0):
        return a + b + c

obj = Calculator()

print(obj.add(5))       
print(obj.add(5, 10))    
print(obj.add(5, 10, 15))

# 2. Method Overridding
class Parent:
    def show(self):
        print("This is Parent class method")

class Child(Parent):
    def show(self):
        print("This is Child class method")

obj = Child()
obj.show()

# Q11). Write a Python program to connect to an SQLite3 database, create a table, insert data, and
# fetch data.
# Ans.

import sqlite3

try:
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    print("Connected to database")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        marks INTEGER
    )
    """)
    print("Table created")

    students_data = [
        ("Kaushal", 85),
        ("Ravi", 90),
        ("Amit", 78)
    ]

    cursor.executemany("INSERT INTO students (name, marks) VALUES (?, ?)", students_data)
    conn.commit()
    print("Data inserted")

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    print("\nStudent Records:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Marks: {row[2]}")

except Exception as e:
    print("Error:", e)

finally:
    conn.close()
    print("\nConnection closed")

# Q12).  Write a Python program to search for a word in a string using re.search().
# Ans.

import re

text = input("Enter a sentence: ")
word = input("Enter word to search: ")
match = re.search(word, text)

if match:
    print(f"'{word}' found in the string at position {match.start()}")
else:
    print(f"'{word}' not found in the string.")

# Q13). Write a Python program to match a word in a string using re.match().
# Ans.    

import re

text = input("Enter a sentence: ")
word = input("Enter word to match: ")
match = re.match(word, text)

if match:
    print(f"'{word}' matched at the beginning of the string.")
else:
    print(f"'{word}' did not match at the beginning.")