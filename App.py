#se importa la clase flask y funcion para renderizar vistas, para manejar urls, ademas de enviar mensajes a las vistas
from flask import Flask, render_template, request, redirect, url_for, flash
#se importa la clase de mysql es necesario para llevar a cabo conexion
from flask_mysqldb import MySQL

#Conexion con MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'              #se establece nombre del host, y los valores de la base de datos
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'
mysql = MySQL(app)                                  #se conservan las conexiones de mysql en variable, se entrega como parametro de conexion las variables de app

#Configuracion de sesiones, debe existir una sesion para enviar mensajes flash
app.secret_key = 'miclavesecreta'

#zona de rutas y controladores
@app.route('/')                                     #cuando inicie el home de la app ingresa a la funcion index
def Index():
    cur = mysql.connection.cursor()                 #creamos un cursor para hacer consultas en la base de datos
    cur.execute('SELECT * FROM contactos')          #creamos la consulta que llenará nuestra tabla
    datos = cur.fetchall()                          #almacenamos los datos de la consulta en una variable
    return render_template('index.html', contactos = datos)     #enviamos la variable a ser renderizada

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
        
        flash('Contacto agregado satisfactoriamente')   #texto que se envia para mostrar en la vista
        return redirect(url_for('Index'))           #redireccionamos a la funcion que procesa en este caso Index

@app.route('/EditarContactos/<id>')                     #recibimos el valor extra y lo guardamos en la variable id
def Obtener_Contacto(id):
    cur = mysql.connection.cursor()                     #generamos un cursor que se conecte con la base de datos
    cur.execute('SELECT * FROM contactos WHERE id = {0}'. format(id))   #ejecutamos la consulta a la base de datos
    dato = cur.fetchall()                               #guardamos los datos en una variable
    return render_template('EditarContactos.html', contacto = dato[0])  #renderizamos la vista para editar contactos                      

@app.route('/Actualizar/<id>', methods=['POST'])        #se define la ruta que se manejara y el tipo de metodo
def Actualizar_Contacto(id):
    if (request.method == 'POST'):                      #obtenemos los datos del formulario
        Nombre = request.form["Nombre"]
        Telefono = request.form['Telefono']
        Mail = request.form['Mail']
    cur = mysql.connection.cursor()                     #creamos el cursor que realiza la conexion a la base de datos
    cur.execute("""                                     
         UPDATE contactos 
         SET Nombre = %s,
             Telefono = %s,
             Mail = %s
         WHERE id = %s
    """, (Nombre, Telefono, Mail, id))                  #generamos la consulta a la base de datos, se usan tres comillas para hacer uso de saltos de linea
    mysql.connection.commit()                           #guardamos los cambios en la base de datos
    flash('Contacto Actualizado Correctamente')         #enviamos un mensaje mediante flash
    return redirect(url_for('Index'))                   #redirigimos a la funcion Index

@app.route('/BorrarContactos/<string:id>')              #en la ruta recibimos un string que lo llamaremos id
def BorrarContactos(id):
    cur = mysql.connection.cursor()                     #creamos un cursor para hacer consultas a la base de datos
    cur.execute('DELETE FROM contactos WHERE id = {0}'. format(id))     #ejecutamos la funcion que borra pasandole el dato id
    mysql.connection.commit()

    flash('Contacto eliminado satisfactoriamente')      #texto que se envia a la vista para mostrarlo
    return redirect(url_for('Index'))                   #redireccionamos con la funcion Index
#fin de la zona de rutas


if __name__ == '__main__':
    app.run(port = 8000, debug = True)        #se corre la app y se entrega un puerto de servidor, ademas se activa el debuger

