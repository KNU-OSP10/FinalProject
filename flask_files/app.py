from crypt import methods
from multiprocessing.sharedctypes import Value
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
@app.route('/')
def index():
    conn = psycopg2.connect(
            host = "20.84.55.133",
            database = "seunghwan",
            user = "seunghwan",
            password = "seunghwan",
            port=5432
            )
    cur=conn.cursor()
    cur.execute('select rank() over (order by see desc) as rank,itemname,min from pharmacy_schema.pills_list join (select drug,min(price) from pharmacy_schema.drug_ranking22 group by drug) as a on pills_list.itemname=a.drug order by see desc limit 5;'
    )
    medi=cur.fetchall()
    cur.close()
    conn.close()
    return render_template('base_db.html', medi=medi)

# 지도 창
@app.route('/pharmacy_map')
def map():
    return render_template('pharmacy_map.html')

# 지도 검색 후 나오는 창
@app.route('/pharmacy_map_methodisTrue', methods=['POST'])
def map_methodisTrue():
    lat = []
    lon = []
    if request.method == 'POST':
        search_pill = request.form['search_pill']
        con = psycopg2.connect(
            host = "20.84.55.133",
            database = "seunghwan",
            user = "seunghwan",
            password = "seunghwan",
            port=5432
            )

        cur = con.cursor()
        
        cur.execute("select (lat) from pharmacy_schema.bukku_list where name like '%{}%'".format(search_pill))
        lat = cur.fetchall()
        con.commit()
        
        global latitude
        global longitude
        global pharmacy_name
        if len(lat) == 1 or len(lat) == 2:
            latitude = (str(lat[0]).replace('(', '')).replace(',)','')

        cur.execute("select (long) from pharmacy_schema.bukku_list where name like '%{}%'".format(search_pill))
        lon = cur.fetchall()
        con.commit()
        
        if len(lon) == 1 or len(lon) == 2:
            longitude = (str(lon[0]).replace('(', '')).replace(',)','')

        cur.execute("select (name) from pharmacy_schema.bukku_list where name like '%{}%'".format(search_pill))
        name = cur.fetchall()
        con.commit()
        
        if len(name) == 1 or len(name) == 2:
            pharmacy_name = (str(name[0]).replace('(', '')).replace(',)','')
            

        cur.close()
        con.close()

        print(len(lat))
        if len(lat) == 0:
            return render_template('pharmacy_map.html')
        else:
            return render_template('pharmacy_map_methodisTrue.html', search_pill_lat=latitude, search_pill_long=longitude, name=pharmacy_name)


@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/drugFind')
def drugFind():
    return render_template('testDrug.html')

@app.route('/pharmFind')
def pharmFind():
    return render_template('testPharm.html')

@app.route('/reporting', methods = ['GET'])
def reporting(): # html에서 form 받아서 DB에 집어넣는 과정 완성
    con = psycopg2.connect(
        host = "20.84.55.133",
        database = 'seunghwan',
        user = "seunghwan",
        password = "seunghwan",
        port = 5432
    )
    cur = con.cursor()
    
    drug = request.args.get("drugName","",str)
    pharmacy = request.args.get("pharmName","",str)
    price = request.args.get("price","0",int)
    description = request.args.get("description","",str)
    
    query = "insert into pharmacy_schema.report(drug,pharmacy,price,description) values('{0}','{1}','{2}','{3}')".format(drug,pharmacy,price,description)
    cur.execute(query)
    
    con.commit()
    cur.close()
    con.close()
    return render_template('successInput.html')

if __name__=='__main__':
    app.run('0.0.0.0', port=5000, debug=True)
