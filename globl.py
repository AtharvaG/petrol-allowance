import mysql.connector

cnx = mysql.connector.connect(user='root', password='gomya', database ='Petrol')
cursor = cnx.cursor(buffered = True)

cnx.commit()

cursor.close()
cnx.close()