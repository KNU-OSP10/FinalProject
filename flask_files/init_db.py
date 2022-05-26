import os
import psycopg2

conn=psycopg2.connect(
	host="localhost",
	database="medi",
	user=os.environ['DB_USERNAME'],
	password=os.environ['DB_PASSWORD'])

cur=conn.cursor()

cur.execute('DROP TABLE IF EXISTS medi;')
cur.execute('CREATE TABLE medi (m_id serial PRIMARY KEY,'
					'mediname varchar(150) NOT NULL,'
					'avgprice integer NOT NULL DEFAULT 0,'
					'count integer NOT NULL DEFAULT 0);')
					
						
					
						

cur.execute('INSERT INTO medi (mediname,avgprice,count)'
		'VALUES (%s, %s, %s)',
		('tylenol',5000,234))
cur.execute('INSERT INTO medi (mediname,avgprice,count)'
		'VALUES (%s, %s, %s)',
		('vitamin',6000,500))
cur.execute('INSERT INTO medi (mediname,avgprice,count)'
		'VALUES (%s, %s, %s)',
		('tenten',10000,3))
cur.execute('INSERT INTO medi (mediname,avgprice,count)'
		'VALUES (%s, %s, %s)',
		('allertec',3000,10))	
		

conn.commit()

cur.close()
conn.close()
