from flask import Flask, render_template, request, redirect, jsonify, Response
from connect import cursor, db
import pymysql

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'my-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'

db = pymysql.connect(
    user="jncpa3or_prod",
    passwd="password98@",
    host="103.195.185.104",
    database="jncpa3or_dev"
)

cursor = db.cursor()


@app.route('/', methods=['GET'])
def index():

    cursor.execute("SELECT id, title FROM learnt WHERE DATE(timestamp) = CURDATE()")
    data = cursor.fetchall()

    return render_template("index.html", data=data)

@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == "GET":
        return render_template("add.html")

    elif request.method == "POST":

        title = request.form['title']
        desc = request.form['desc']

        cursor.execute("INSERT INTO learnt(title, description) VALUES('%s', '%s')" % (title, desc))
        db.commit()

        return jsonify({"ret": "success"})

@app.route('/check', methods=['GET', 'POST'])
def check():

    if request.method == "GET":
        return render_template("check.html")

    elif request.method == "POST":

        date = request.form['date']
        title = request.form['title']

        if date == "-1":
            cursor.execute("SELECT id, title FROM learnt WHERE title='%s'" % title)
        elif title == "-1":
            cursor.execute("SELECT id, title FROM learnt WHERE DATE(timestamp)='%s'" % date)
        else:
            cursor.execute("SELECT id, title FROM learnt WHERE DATE(timestamp)='%s' AND title='%s'" % (date, title))

        data = cursor.fetchall()

        return jsonify({"data": data})

@app.route('/detail', methods=['GET'])
def detail():

    id = int(request.args.get('id'))

    cursor.execute("SELECT title, description FROM learnt WHERE id=%d" % id)
    data = cursor.fetchone()

    return render_template("detail.html", title=data[0], desc=data[1])

if __name__ == "__main__":
    app.run()
