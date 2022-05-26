import psycopg2
from flask import Flask, request, render_template

#connect to the DB
con = psycopg2.connect(
    host = "localhost",
    database = "reportDB",
    user = "postgres",
    password = "2896"
)
# cursor
cur = con.cursor()

cur.execute("insert into public.customers(name, email) values ('Bob Brown','bob@brown.com')")

# execute query
cur.execute("select id, name from public.customers")

rows = cur.fetchall()

for r in rows : 
    print("id {0} name {1}".format(r[0],r[1]))
    
#commit the transaction
con.commit()  # 커밋을 해줘야 실제 데이터베이스에 반영된다!
  
#close the cursor
cur.close()    

#close the connection
con.close()
