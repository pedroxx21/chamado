from flask import Flask, render_template, request, session,redirect, jsonify,url_for
from flask_wtf import CSRFProtect 
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from datetime import date

app = Flask(__name__)
app.secret_key = b'40203b1ce74ad29c891d33f0afef4d2c'
csrf = CSRFProtect(app) 
bcrypt = Bcrypt(app)

'''
    Configurações da string de conexão
'''
app.config['MYSQL_HOST'] = 'db-mysql-nyc3-13529-do-user-15782594-0.c.db.ondigitalocean.com'
app.config['MYSQL_USER'] = 'doadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_be6DYBLeXon1FMWpWWZ'
app.config['MYSQL_DB'] = 'db_pedro'
app.config['MYSQL_PORT'] = 25060

mysql = MySQL(app)

#app.secret_key = 'ola brasil amado'



'''
    Rota principal da aplicação
'''
@app.route("/")
def login():
    return render_template('login.html', is_home=True)


'''
    Rota da dashboard
'''
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html',is_home=False)



'''
    Rota do formulario
'''
@app.route("/consumidor/formulario")
def formulario():
    return render_template('formulario.html', is_home=False)



'''
    Insert registros na tabela de tb_consumidor
'''
@app.route("/consumidor/insert", methods = ['POST'])
def consumidorInsert():

    if request.method == 'POST':
        nomeDoConsumidor = request.form['nomeDoConsumidor']
        email = request.form['email']
        celular = request.form['celular']
        senha = request.form['senha']
        dataAtual = date.today()

        hashPassword = bcrypt.generate_password_hash(senha).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tb_consumidor (nomeDoConsumidor, email, celular, senha, created_at) VALUES (%s, %s, %s, %s, %s)", (nomeDoConsumidor, email, int(celular), hashPassword, dataAtual))
        mysql.connection.commit()

        return render_template('login.html', is_home=True,mensagem = "Consumidor inserido com sucesso")



'''
    Login do usuario
'''
@app.route("/login", methods = ['POST'])
def loginConsumidor():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("Select * from tb_consumidor WHERE email= %s",(email, ))
        usuario = cur.fetchone()
        cur.close

        return jsonify({'error': usuario}), 200

        stored_password_hash = usuario[4]

        if bcrypt.check_password_hash(stored_password_hash.encode('utf-8'), senha.encode('utf-8')):
            session['user'] = usuario[1]
            return redirect(url_for('dashboard'))
        else:
            return jsonify({'error': 'Invalid password'}), 401
    else:
        return jsonify({'error': 'User not found'}), 404
        


'''
    Retornar todos os registros cadastrados na tabela de consumidor
'''
@app.route("/consumidor/lista")
def listaConsumidor():
    cur = mysql.connection.cursor()
    cur.execute("Select * from tb_consumidor")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', consumidor = data)


if __name__ == '__main__':
    app.run(debug=True)