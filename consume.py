from flask import Flask, render_template
import json
import requests

app = Flask("__main__")


@app.route("/", methods=['GET'])
def homepage():
    r = requests.get("http://richardobiye.com/py/api/employees.php")
    myresponse = r.content
    res_to_json = json.loads(myresponse)
    return render_template('employees.html', data=res_to_json)


# @app.route("/employee",methods =['GET'])
# def singleemployee():
#     r= requests.get("http://richardobiye.com/py/api/employee.php")
#     myresponse = r.content
#     res_to_json = json.loads(myresponse)
#     print("Single employee",res_to_json)
#     return render_template('employees.html',data = res_to_json)

if __name__ == "__main__":
    app.run(debug=True)
