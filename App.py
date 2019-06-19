from flask import Flask, render_template, request   #se importa la clase flask y funcion para renderizar vistas
from flask_mysqldb import MySQL                     #se importa la clase de mysql es necesario para llevar a cabo conexion

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'              #se establece nombre del host, y los valores de la base de datos
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'
mysql = MySQL(app)                                  #se conservan las conexiones de mysql en variable, se entrega como parametro de conexion las variables de app

@app.route('/')                                     #cuando inicie el home de la app ingresa a la funcion index
def Index():
    return render_template('index.html')

@app.route('/AñadirContactos', methods=['POST'])    #se declara la ruta y el metodo por el cual se llamara la funcion
def AñadirContactos():
    if request.method == 'POST':                    #se pregunta si el request ha sido enviado por un metodo post
        Nombre = request.form['Nombre']             #se envian los valores y se guardan los valores de nombre a una nueva variable
        Telefono = request.form['Telefono']
        Mail = request.form['Mail']
        cur = mysql.connection.cursor()             #se crea un cursor que permite revisar las consultas de MYSQL
        cur.execute('INSERT INTO contactos (Nombre,Telefono,Mail) VALUES (%s, %s, %s)', 
        (Nombre, Telefono, Mail))
        mysql.connection.commit()
        
        return 'Recibido'

@app.route('/EditarContactos')
def EditarContactos():
    return 'EditarContactos'

@app.route('/BorrarContactos')
def BorrarContactos():
    return 'BorrarContactos'

if __name__ == '__main__':
    app.run(port = 8000, debug = True)        #se corre la app y se entrega un puerto de servidor, ademas se activa el debuger

