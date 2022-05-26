from crypt import methods
from multiprocessing.sharedctypes import Value
from flask import Flask, render_template, request
import psycopg2

        
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('hello.html')

@app.route('/write_price')
def write():
    return render_template('writePrice.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/reporting', methods = ['GET'])
def reporting():
    con = psycopg2.connect(
        host = "localhost",
        database = 'reportDB',
        user = "postgres",
        password = "2896"
    )
    cur = con.cursor()
    
    drug = request.form('drugName')
    pharmacy = request.form('pharmName')
    price = request.form('price')
    description = request.form('description')
    
    query = "insert into public.reportDB(drug,pharmacy,price,description) value({0},{1},{2},{3})".format(drug,pharmacy,price,description)
    cur.execute(query)
    
    con.commit()
    cur.close()
    con.close()
    
