from flask import Flask, render_template, redirect, request, url_for
import sqlite3
import datetime
from random import randint

'''import sys
path = '/home/thepoppycat/2020_STW1'
if path not in sys.path:
   sys.path.insert(0, path)'''


app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_temp', methods=['GET', 'POST'])
def check():
    user_temp = request.form.get('temp')
    unit = request.form.get('unit')
    try:
        temp = float(user_temp)
        if unit=="2": # Convert to celsius
            temp-=32
            temp=temp*5/9

        if(temp>=38):
            text = "Your temperature is abonormally high. you may have a fever. Go drink some water and see a doctor."
        else:
            text = "You do not have a symptom of the virus. "
            text += "However, you may want to go get yourself checked if you have more than one of the symptoms below. "
            text += "Either way, rest well and drink lots of water."
        curr = datetime.datetime.now()
        connection = sqlite3.connect("sqlite.db")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO temperatures VALUES ("{0}", {1})'.format(str(curr), temp))
        connection.commit()
        connection.close()
    except:
        temp=randint(27, 41)
        text = "You did not input a number, try again"
    #return redirect(url_for("index", text=text, temp=temp))
    return render_template('index.html', text=text, user_temp=user_temp, temp_celsius=temp)


@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)



