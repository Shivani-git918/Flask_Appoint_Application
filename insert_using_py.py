import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Loveulife@12",
    database="py_pro"
)
mycursor= db.cursor()
insert_query = "INSERT INTO form (name, age,contact_number, date, specialist) VALUES (%s, %s,%s, %s, %s)"
data = ("krishna kapila", "25", "0987654321", "2023-01-08", "therapist")
mycursor.execute(insert_query, data)
db.commit()

print(mycursor.rowcount , "record inserted")
