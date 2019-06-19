from flask import Flask                       #se importa la clase flask

app = Flask(__name__)

@app.route('/')                               #cuando inicie el home de la app ingresa a la funcion index
def Index():
    return 'Hola mundo'

@app.route('/AñadirContactos')
def AñadirContactos():
    return 'AgregarContacto'

@app.route('/EditarContactos')
def EditarContactos():
    return 'EditarContacto'

@app.route('/BorrarContactos')
def BorrarContactos():
    return 'BorrarContactos'

if __name__ == '__main__':
    app.run(port = 8000, debug = True)        #se corre la app y se entrega un puerto de servidor, ademas se activa el debuger

