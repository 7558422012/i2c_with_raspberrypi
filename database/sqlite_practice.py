import sqlite3
conn = sqlite3.connect("mydata.db") #connection has been created
c=conn.cursor()
c.execute("""CREATE TABLE moti(c_name text,c_lastname text,c_email text)""")
conn.commit()
conn.close()