from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL, MySQLdb
from flask_session import Session
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Cargar variables de entorno desde un archivo .env
load_dotenv()

#Conexion a BDD
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST') 
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB') 
mysql = MySQL(app)

#rutas
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/registro")
def regitro():
    return render_template("registre.html")

@app.route("/pagina-inicio")
def inicio():
    return render_template("inicio.html")


#carga de casos
@app.route("/cargadecasos", methods=['POST'])
def carga_de_casos():
    if  request.method == 'POST':
        telefono = request.form['telefono']
        nombre = request.form['nombre']
        apellido= request.form['apellido']
        barrio= request.form['barrio']
        direccion= request.form['direccion']
        tipo_de_caso= request.form['TipoDecaso']
        
        cur = mysql.connection.cursor()    
        
        cur.execute('''INSERT INTO grupos (telefono, nombre, apellido, barrio, direccion,casos)
                    VALUES (%s, %s, %s, %s,%s,%s)'''
                    , (telefono,nombre,apellido,barrio,direccion,tipo_de_caso))
        
        mysql.connection.commit()
        
        
        return render_template ('inicio.html')



if __name__=="__main__":
    app.secret_key='llave secreta'
    app.run(debug=True)