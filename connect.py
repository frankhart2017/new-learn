import mysql.connector

db = mysql.connector.connect(
    user="jncpa3or_prod",
    passwd="password98@",
    host="103.195.185.104",
    database="jncpa3or_dev"
)

cursor = db.cursor()

def reconnect():
    db = mysql.connector.connect(
        user="jncpa3or_prod",
        passwd="password98@",
        host="103.195.185.104",
        database="jncpa3or_dev"
    )

    cursor = db.cursor()
