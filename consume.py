from flask import Flask, render_template, request, redirect, jsonify
import json
import requests
from flask_mysqldb import MySQL

app = Flask("__main__")

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "employeeapi"
mysql = MySQL(app)


@app.route("/employeeitems", methods=['GET'])
def employeeitems():
    r = requests.get("https://richardobiye.com/py/api/employeeitems.php")
    myresponse = r.content
    res_to_json = json.loads(myresponse)
    cur = mysql.connection.cursor()

    for employee in res_to_json:
        idNumbers = employee['idNumbers']
        name = employee['name']
        age = employee['age']
        sex = employee['sex']
        maritalStatus = employee['maritalStatus']
        dateOfBirth = employee['dateOfBirth']
        laptop = employee['laptop']
        ram = laptop['ram']
        ssd = laptop['ssd']
        storage = laptop['storage']
        screenSize = laptop['screenSize']
        speed = laptop['speed']
        cur.execute("INSERT into emp(idNumbers,name,age,sex,maritalStatus,dateOfBirth) VALUES(%s,%s,%s,%s,%s,%s) ",
                    (idNumbers, name, age, sex, maritalStatus, dateOfBirth))
        cur.execute("INSERT into emp_laptops(idNumbers,ram,ssd,storage,screenSize,speed) VALUES(%s,%s,%s,%s,%s,%s) ",
                    (idNumbers, ram, ssd, storage, screenSize, speed))
        mysql.connection.commit()
    cur.close()
    return render_template('emp_db.html')
    # return render_template('employees.html', data=res_to_json)


# @app.route("/employee",methods =['GET'])
# def singleemployee():
#     r= requests.get("http://richardobiye.com/py/api/employee.php")
#     myresponse = r.content
#     res_to_json = json.loads(myresponse)
#     print("Single employee",res_to_json)
#     return render_template('employees.html',data = res_to_json)

@app.route("/listall", methods=['GET'])
def getemployeebyid():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM emp")
        userdata = []
        status = 1
        message = "No employees  Found"

        if result > 0:
            status = 0
            userdata = cur.fetchall()
            message = "User Found successfully"
        return jsonify({"status": status, "message": message, "userdata": userdata})


@app.route("/f", methods=['GET'])
def homepage():
    r = requests.get("https://richardobiye.com/py/api/employeeitems.php")
    myresponse = r.content
    res_to_json = json.loads(myresponse)
    cur = mysql.connection.cursor()

    for employee in res_to_json:
        idNumbers = employee['idNumbers']
        name = employee['name']
        age = employee['age']
        sex = employee['sex']
        maritalStatus = employee['maritalStatus']
        dateOfBirth = employee['dateOfBirth']

        cur.execute("INSERT into emp(idNumbers,name,age,sex,maritalStatus,dateOfBirth) VALUES(%s,%s,%s,%s,%s,%s) ",
                    (idNumbers, name, age, sex, maritalStatus, dateOfBirth))
        mysql.connection.commit()
    cur.close()
    return render_template('emp_db.html')


if __name__ == "__main__":
    app.run(debug=True)
