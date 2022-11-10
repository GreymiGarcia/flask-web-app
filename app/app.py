from flask import Flask,render_template,request,url_for,redirect,jsonify
from flask_mysqldb import MySQL

app=Flask(__name__)

#MYSQL Conexion
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'abaco'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.before_request
def before_request():
    print("Before request!!")

@app.after_request
def after_request(response):
    print("After request!!")
    return response

@app.route('/')
def index():
    cursos = ['php','java','css','html','bootstrap']
    data={
        'titulo':'index',
        'bienvenida':'Saludos!',
        'cursos':cursos,
        'numero_cursos':len(cursos)
    }
    return render_template('index.html',data=data)

@app.route('/contact/<name>/<int:age>')
def contact(name,age):
    data={
        'title':'Contact',
        'name':name,
        'age':age
    }
    return render_template('contact.html',data=data)


def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return 'OK'

@app.route('/courses')
def courses_list():
    data={}
    # try:
    cursor = mysql.connection
    cur = cursor.cursor()
    sql="SELECT * FROM ` courses` ORDER BY name ASC;"
    cur.execute(sql)
    courses = cur.fetchall()
    data['Courses']=courses
    data['message']='Success'
    # except Exception as ex:
    #     data['message']='Error...'
    return jsonify(data)

def not_found(error):
    # return render_template('404.html'), 404
    return redirect(url_for('index'))

if __name__=='__main__':
    app.add_url_rule('/query_string',view_func=query_string)
    app.register_error_handler(404,not_found)
    app.run(debug=True,port=5000)