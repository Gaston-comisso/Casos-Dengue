from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Cargar variables de entorno desde un archivo .env
load_dotenv()

# Configuración de conexión a MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

# Ruta para la carga de casos
@app.route("/cargadecasos", methods=['POST'])
def carga_de_casos():
    if request.method == 'POST':
        telefono = request.form['telefono']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        barrio = request.form['barrio']
        direccion = request.form['direccion']
        tipo_de_caso = request.form['TipoDecaso']
        
        # Insertar datos en la base de datos
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO grupos (telefono, nombre, apellido, barrio, direccion, casos)
                    VALUES (%s, %s, %s, %s, %s, %s)''',
                    (telefono, nombre, apellido, barrio, direccion, tipo_de_caso))
        mysql.connection.commit()
        cur.close()
        flash('Los datos se han cargado correctamente', 'success')

        # Redirigir a la página de inicio después de la inserción
        return redirect(url_for('pagina_inicio'))

# ruta para la eliminacion de casos
@app.route('/delete/<int:id>')
def eliminar_producto(id):
    cur = mysql.connection.cursor()    
    cur.execute('DELETE FROM grupos WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    flash('Eliminado correctamente', 'danger')
    return redirect(url_for('pagina_inicio'))

# Ruta para la página de inicio
@app.route("/pagina-inicio")
def pagina_inicio():
    # Obtener todos los registros de la tabla después de la inserción
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM grupos")
    grupos = cur.fetchall()
    cur.close()
    # Pasar los datos a la plantilla para mostrarlos
    return render_template("inicio.html", grupos=grupos)

# Ruta y función para la edición de casos
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_grupo(id):
    if request.method == 'POST':
        telefono = request.form['telefono']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        barrio = request.form['barrio']
        direccion = request.form['direccion']
        tipo_de_caso = request.form['TipoDecaso']

        # Actualizar los datos en la base de datos
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE grupos
                       SET telefono = %s, nombre = %s, apellido = %s, barrio = %s, direccion = %s, casos = %s
                       WHERE id = %s''',
                    (telefono, nombre, apellido, barrio, direccion, tipo_de_caso, id))
        mysql.connection.commit()
        cur.close()
        flash('Datos actualizados correctamente', 'success')

        # Redirigir a la página de inicio después de la actualización
        return redirect(url_for('pagina_inicio'))
    
    # Obtener los datos del grupo a editar
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM grupos WHERE id = %s", (id,))
    grupo = cur.fetchone()
    cur.close()

    # Renderizar el formulario de edición con los datos actuales
    return render_template('inicio.html', grupo=grupo)


# Rutas adicionales (puedes definir más rutas según tus necesidades)
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/registro")
def registro():
    return render_template("registre.html")

# Configurar la clave secreta para la aplicación
app.secret_key = 'llave secreta'

if __name__ == "__main__":
    app.run(debug=True)
