from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL, MySQLdb
from flask_session import Session
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Cargar variables de entorno desde un archivo .env
load_dotenv()



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




if __name__=="__main__":
    app.secret_key='llave secreta'
    app.run(debug=True)