import sqlite3

try:
    db=sqlite3.connect("demo.db")
    print("Datbase craeted")
except Exception as e:
    print(e)

table_create ="Create table poduct_master(id integer primary " \
"key autoincrement,name text, city text)" 
try:
    db.execute(table_create)
except Exception as e:
    print(e)    

insert_data ="Insert into poduct_master(name,city)values" \
"('Kaushal','Jamnagar'),('Raj','Rajkot)')" 
try:
    db.execute(insert_data)
    db.commit()
    print("Record insreted")
except Exception as e:
    print(e)    
    