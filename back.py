from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
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
#----seccion login----

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor inicia sesión para acceder a esta página."

#Modelo de usuario
class User(UserMixin):
    def __init__(self, id,nombre,telefono, email, password):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, telefono, email, contraseña FROM usuarios WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1], user[2],user[3],user[4])
    return None

#Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        password = request.form['password']
        
        # Verificar si el email ya está registrado
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            cur.close()
            flash('El email ya existe', 'error')
            return redirect(url_for('register'))
        
        # Insertar el nuevo usuario en la base de datos
        cur.execute("INSERT INTO usuarios (nombre,telefono, email, contraseña) VALUES (%s, %s, %s, %s)", (nombre,telefono,email, password))
        mysql.connection.commit()
        cur.close()
        
        flash('Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    
    return render_template('registre.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombre,telefono, email, contraseña FROM usuarios WHERE email = %s AND contraseña = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            user_obj = User(user[0], user[1], user[2],user[3],user[4])
            login_user(user_obj)
            flash('inicio de sesion exitoso!', 'login_success')
            return redirect(url_for('pagina_inicio'))
        else:
            flash('Credenciales Invalidas', 'login_error')
    return render_template('login.html')



#Ruta de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('has cerrado sesión')
    return redirect(url_for('pagina_inicio'))

#----seccion main----
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
        flash('Los datos se han cargado correctamente', 'carga_success')

        # Redirigir a la página de inicio después de la inserción
        return redirect(url_for('pagina_inicio'))

# ruta para la eliminacion de casos
@app.route('/delete/<int:id>')
def eliminar_producto(id):
    cur = mysql.connection.cursor()    
    cur.execute('DELETE FROM grupos WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()
    flash('Eliminado correctamente', 'delete_danger')
    return redirect(url_for('pagina_inicio'))

# Ruta para la página de inicio
@app.route("/pagina-inicio")
@login_required
def pagina_inicio():
    # Obtener todos los registros de la tabla después de la inserción
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM grupos")
    grupos = cur.fetchall()
    cur.close()
    flash(f'bienvenido {current_user.nombre}', 'info')
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
    if current_user.is_authenticated:
        return redirect(url_for('pagina_inicio')) #si el usuario esta logueado, puede ir a la pagina de inicio directamente
    return render_template("login.html")



# Configurar la clave secreta para la aplicación
app.secret_key = 'llave secreta'

if __name__ == "__main__":
    app.run(debug=True)
