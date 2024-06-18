from flask import Flask, render_template, request, session, redirect, jsonify, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from datetime import date

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db-mysql-nyc3-13529-do-user-15782594-0.c.db.ondigitalocean.com'
app.config['MYSQL_USER'] = 'doadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_be6DYBLeXon1FMWpWWZ'
app.config['MYSQL_DB'] = 'db_pedro'
app.config['MYSQL_PORT'] = 25060

mysql = MySQL(app)

app.secret_key = 'ola brasil amado'
bcrypt = Bcrypt(app)

@app.route('/')
def login():
    return render_template('login.html', is_home=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', is_home=True)

@app.route('/consumidor/formulario')
def formulario():
    return render_template('formulario.html', is_home=True)

@app.route('/consumidor/insert', methods = ['POST'])
def consumidorInsert():

    if request.method == 'POST':
        nomeDoconsumidor = request.form['nomeDoConsumidor']
        email = request.form['email']
        celular = request.form['celular']
        senha = request.form['senha']
        dataAtual = date.today()

        hashPassword = bcrypt.generate_password_hash(senha).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO db_Consumidor (nome, email, celular, senha, created_at)VALUES(%s,%s,%s,%s,%s)', (nomeDoconsumidor, email, int(celular),hashPassword,dataAtual))
        mysql.connection.commit()

        return render_template('login.html', is_home=True, mensagem = 'consumidor')
    
    
if __name__ == '__main__':
    app.run(debug=True)