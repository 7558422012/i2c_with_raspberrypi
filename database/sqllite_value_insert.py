import sqlite3
conn=sqlite3.connect("mydata.db")
c=conn.cursor()
c.execute("INSERT INTO customer VALUES('rohit','sharma','shivay@gmail.com')")
conn.commit()
conn.close()