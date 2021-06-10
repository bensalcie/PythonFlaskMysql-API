from flask import Flask, render_template, request, redirect,jsonify
import yaml
from flask_mysqldb import MySQL

# configure mysql

app = Flask(__name__)

db = yaml.load(open("db.yaml"))
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flaskapp"

mysql = MySQL(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # fetch form data
        userdetails = request.form

        username = userdetails['username']
        email = userdetails['email']
        password = userdetails['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT into users(username,email,password) VALUES(%s,%s,%s) ", (username, email, password))
        mysql.connection.commit()
        cur.close()
        return redirect("/users")

    return render_template("index.html")


@app.route("/users")
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * from users ORDER BY id DESC")
    if resultValue > 0:
        userdetails = cur.fetchall()
        return render_template("users.html", userdetails=userdetails)


if __name__ == "__main__":
    app.run(debug=True)
