from flask import Flask, render_template, request, redirect, jsonify
import yaml
import json
from flask_mysqldb import MySQL

# configure mysql

app = Flask(__name__)

db = yaml.load(open("db.yaml"))
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "uflaskapp"

mysql = MySQL(app)


@app.route("/create", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # fetch form data
        userdetails = request.json
        username = userdetails['username']
        email = userdetails['email']
        password = userdetails['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT into users(username,email,password) VALUES(%s,%s,%s) ", (username, email, password))
        mysql.connection.commit()
        cur.close()
        return jsonify({"response": "User Saved Successfully"})

    # return render_template("index.html")


@app.route("/users")
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * from users ORDER BY id DESC")
    if resultValue > 0:
        userdetails = cur.fetchall()
        return jsonify({"status": 0, "data": userdetails, "message": "Found {} records".format(resultValue)})
    else:
        return jsonify(
            {"status": 1, "data": "[]", "response": "No records were found", "message": "No records were found"})


if __name__ == "__main__":
    app.run(debug=True)
