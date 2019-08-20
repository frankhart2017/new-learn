from flask import Flask, render_template, request, redirect, jsonify, Response, Markup
from connect import cursor, db, reconnect

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'my-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/', methods=['GET'])
def index():

    try:
        cursor.execute("SELECT id, title FROM learnt WHERE DATE(timestamp) = CURDATE()")
    except:
        reconnect()
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

    return render_template("detail.html", title=data[0], desc=Markup(data[1]))

if __name__ == "__main__":
    app.run()
