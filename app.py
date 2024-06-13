# entrada a la aplicacion
from flask import Flask, redirect, render_template, request, session, url_for
import config
from flask_mysqldb import MySQL #paquete conexion de  MYSQL

#--------------------------------------------------------------------------------------------------------------------------
#*                                        app y su conexion la DB                                          
#--------------------------------------------------------------------------------------------------------------------------

app = Flask(__name__) # app instancia de Flask
mysql = MySQL(app) #conexion de app a la base de datos

# configuracion de la app con los datos para la conexion
app.config["SECRET_KEY"] = config.HEX_SEC_KEY
app.config["MYSQL_HOST"] = config.MYSQL_HOST
app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = config.MYSQL_DB



#--------------------------------------------------------------------------------------------------------------------------
#*                                                  RUTAS
#--------------------------------------------------------------------------------------------------------------------------

# todo   RUTA HOME
@app.route('/', methods=['GET']) 
def home():
    return render_template('index.html')

#TODO RUTA LOGIN
@app.route('/login', methods=['POST']) 
def login():
    # datos del formulario
    email = request.form['email']
    password = request.form['password']
    
    cur = mysql.connection.cursor() # conexion a la base de datos
    cur.execute("SELECT * FROM clientes WHERE email = %s AND password = %s", (email, password))
    user = cur.fetchone() # aqui se guarda la consulta
    print(user)
    cur.close() # cerrar la base de datos
    
    if user is not None: # si el usuario existe
        session["email"] = email
        session["password"] = password
        session["nombre"] = user[1]
        
        return redirect(url_for('turnos')) #si coinciden los datos de la consulta, redirige a la ruta turnos
    else: 
        return render_template('index.html',message="Usuario o contraseña incorrectos")
    

# TODO RUTA TURNOS
@app.route('/turnos', methods=['GET'])
def turnos():
    return render_template('turnos.html')




#================================================
# El objeto session en Flask (o frameworks similares) 
# es un diccionario que persiste datos entre las solicitudes del mismo usuario. 
# Esto es crucial para mantener el estado de autenticación y 
# otros datos específicos del usuario mientras navega por 
# diferentes páginas de la aplicación.               
#================================================





if __name__ == '__main__':
    app.run(debug=True)  # debug= true para que el servidor se reinicie cada vez que cambia el código.

