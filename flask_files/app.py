# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import json
import psycopg2

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/pharmacy_map')
def map():
    return render_template('pharmacy_map.html')


@app.route('/pharmacy_map_methodisTrue', methods=['POST'])
def map_methodisTrue():
    lat = []
    longitude = []
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
        latitude = (str(lat[0]).replace('(', '')).replace(',)','')
        if len(lat) == 2:
            latitude2 = (str(lat[1]).replace('(', '')).replace(',)','')

        cur.execute("select (long) from pharmacy_schema.bukku_list where name like '%{}%'".format(search_pill))
        lon = cur.fetchall()
        con.commit()
        
        longitude = (str(lon[0]).replace('(', '')).replace(',)','')
        if len(lon) == 2:
            longitude2 = (str(lon[0]).replace('(', '')).replace(',)','')

        cur.close()
        con.close()

        
        if len(lat) == 0:
            return render_template('pharmacy_map.html')
        elif len(lat) == 2:
            return render_template('pharmacy_map_methodisTrue.html', search_pill_lat=latitude, search_pill_lat2=latitude2, search_pill_long=longitude, search_pill_long2=longitude2)
        else:
            return render_template('pharmacy_map_methodisTrue.html', search_pill_lat=latitude, search_pill_long=longitude)

@app.route('/report')
def remote():
    return render_template('report.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

if __name__=='__main__':
    app.run('0.0.0.0', port=5000, debug=True)
