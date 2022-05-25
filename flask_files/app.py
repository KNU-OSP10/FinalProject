from flask import Flask, render_template

        
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/pharmacy_map')
def map():
    return render_template('pharmacy_map.html')

@app.route('/report')
def remote():
    return render_template('report.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')
