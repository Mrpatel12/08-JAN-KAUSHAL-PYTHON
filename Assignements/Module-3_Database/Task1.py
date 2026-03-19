import sqlite3

try:
    db = sqlite3.connect("demo.db")
    print("Database created/connected")
except Exception as e:
    print(e)

table_create = """
CREATE TABLE product_master(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,city TEXT)
"""
try:
    db.execute(table_create)
    db.commit()
    print("Table Craeted")
except Exception as e:
    print(e)

for i in range(2):
    nm = input("Enter the name of the user: ")
    ct = input("Enter the city of the user: ")
    db.execute("INSERT INTO product_master(name, city) VALUES(?, ?)", (nm, ct))
    db.commit()
    print("Record inserted")
 
    id = input("Enter ID to update: ")
    nm = input("Enter new name: ")
    ct = input("Enter new city: ")

    db.execute("UPDATE poduct_master SET name=?, city=? WHERE id=?", (nm, ct, id))
    db.commit()
    print("Record updated")

    
    id = input("Enter ID to delete: ")
    db.execute("DELETE FROM poduct_master WHERE id=?", (id,))
    db.commit()
    print("Record deleted")


