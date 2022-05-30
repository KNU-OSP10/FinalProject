from crypt import methods
from multiprocessing.sharedctypes import Value
from flask import Flask, render_template, request
import psycopg2
import json


def connectDB():
    conn = psycopg2.connect(
        host = "20.84.55.133",
        database = "seunghwan",
        user = "seunghwan",
        password = "seunghwan",
        port=5432
        )
    return conn

app = Flask(__name__)

@app.route('/')
def index():
    con = connectDB()
    
    cur = con.cursor()
    cur.execute('select rank() over (order by see desc) as rank,itemname,min from pharmacy_schema.pills_list join (select drug,min(price) from pharmacy_schema.drug_ranking22 group by drug) as a on pills_list.itemname=a.drug order by see desc limit 5;')
    medi=cur.fetchall()
    cur.close()
    con.close()
    return render_template('base_db.html', medi=medi)

# 지도 창
@app.route('/pharmacy_map')
def map():
    return render_template('pharmacy_map.html')

# 지도 검색 후 나오는 창
@app.route('/pharmacy_map_methodisTrue', methods=['POST'])
def map_methodisTrue():
    find = []
    latitude = []
    longitude = []
    pharmacy_name = []
    if request.method == 'POST':
        
        search_pill = request.form['search_pill']
        con = connectDB()
        cur = con.cursor()
        
        cur.execute("select (lat, long, name) from pharmacy_schema.bukku_list where name like '%{}%'".format(search_pill))
        find = cur.fetchall()
        
        if len(find) >= 1:
            for i in range(len(find)):
                latitude.append(((find[i][0].replace('(', '')).replace(')','')).split(",")[0])
                longitude.append(((find[i][0].replace('(', '')).replace(')','')).split(",")[1])
                pharmacy_name.append(((find[i][0].replace('(', '')).replace(')','')).split(",")[2])

        cur.close()
        con.close()

        if len(find) == 0:
            return render_template('pharmacy_map.html')
        else:
            return render_template('pharmacy_map_methodisTrue.html',data_lat=json.dumps(latitude), data_long=json.dumps(longitude), data_name=pharmacy_name)

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
    con = connectDB()
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

@app.route('/findPharmacy' , methods = ['GET', 'POST'])
def findPharmacy():
    
    if request.method == 'POST':
        con = connectDB()
        cur = con.cursor()
        
        keyword = request.form['pharmName']
        cur.execute("select * from pharmacy_schema.bukku_list where name like '%{0}%'".format(keyword))
        pharmacy = cur.fetchall()
    
        cur.close()
        con.close()
        return render_template('findPharm2.html', pharmacy = pharmacy)
    else:
        return render_template('findPharm.html')

@app.route('/findDrugs', methods = ['GET', 'POST'])
def findDrugs():
    
    if request.method == "POST":
        con = connectDB()
        cur = con.cursor()
        keyword = request.form['drugName']
        cur.execute("select * from pharmacy_schema.pills_list where itemname like '%{0}%'".format(keyword))
        drugs = cur.fetchall()
        
        cur.close()
        con.close()
        return render_template('findDrug2.html', drugs = drugs)
    else:
        return render_template('findDrug.html')

#search창 - 검색 기능 추가하기 전
@app.route('/search')
def search():
    con = connectDB()
    cur = con.cursor()

     if request.method == "POST":
        keyword = request.form['druginput']
        cur.execute("SELECT * FROM pharmacy_schema.pills_list where itemname like '%{0}%'".format(keyword))
        descript = cur.fetchall()
        con.commit()

        cur.execute("SELECT * FROM pharmacy_schema.drug_ranking22 where drug like '%{0}%' order by 3 limit 5".format(keyword))
        ranks = cur.fetchall()
        cur.close()

        con.close()
        return render_template('search.html', descript=descript, ranks=ranks)

#test search - 검색 기능 시험 용
@app.route('/testsearch')
def test():
    return render_template('testsearch.html')

if __name__=='__main__':
    app.run('0.0.0.0', port=5000, debug=True)
