from flask import Flask, render_template

        
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('hello.html')

@app.route('/write_price')
def write():
    return render_template('writePrice.html')
