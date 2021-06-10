from flask import Flask, jsonify, request
import yaml
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "employee"

mysql = MySQL(app)


@app.route("/createemployee", methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        givenvalues = request.json
        name = givenvalues['name']
        age = givenvalues['age']
        sex = givenvalues['sex']
        maritalstatus = givenvalues['maritalstatus']
        dob = givenvalues['dob']
        cur = mysql.connection.cursor()
        cur.execute("INSERT into employee(name,age,sex,maritalstatus,dob) values (%s,%s,%s,%s,%s)",
                    (name, age, sex, maritalstatus, dob))
        cur.connection.commit()
        cur.close()
        return jsonify({"response": "User saved Successfully"})


@app.route("/employees")
def getall():
    cur = mysql.connection.cursor()
    results = cur.execute("SELECT * FROM employee")
    status = 1
    userdata = []

    message = "No Records were found"
    if results > 0:
        status = 0
        message = "Data fetched successfully"
        userdata = cur.fetchall()
    return jsonify({"status": status, "message": message, "userdata": userdata})


@app.route("/employeebyid", methods=['POST'])
def getemployeebyid():
    if request.method == "POST":
        inputdata = request.json
        emp_id = inputdata['id']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM employee WHERE id ='{}' ".format(emp_id))
        userdata = []
        status = 1
        message = "No user Id Found"

        if result > 0:
            status = 0
            userdata = cur.fetchall()
            message = "User id Found successfully"
        return jsonify({"status": status, "message": message, "userdata": userdata})


@app.route("/updateemployee", methods=['POST'])
def updateemployee():
    if request.method == "POST":
        given_data = request.json
        empl_id = given_data['id']
        empl_name = given_data['name']
        empl_age = given_data['age']
        empl_dob = given_data['dob']
        empl_marital_Status = given_data['maritalstatus']
        empl_sex = given_data['sex']

        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE employee SET name= '{}',age='{}',sex='{}',maritalstatus='{}',dob='{}' WHERE id = '{}'".format(
                empl_name, empl_age, empl_sex, empl_marital_Status, empl_dob, empl_id))
        cur.connection.commit()
        cur.close()
        return jsonify({"response": "Updated Successfully"})


@app.route("/delete", methods=['POST'])
def deleteemployee():
    if request.method == "POST":
        givendata = request.json
        employee_id = givendata['id']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM employee WHERE id ='{}'".format(employee_id))
        cur.connection.commit()
        cur.close()
        return jsonify({"response": "User with id {} was deleted successfully".format(employee_id)})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
