from flask import Flask, render_template, request, redirect, session
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a secure key
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'pythontest'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def home():
    if 'email' in session:
        email = session['email']
        return render_template('home.html', email=email)
    else:
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = mysql.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        
        if user:
            session['email'] = email
            return redirect('/')
        else:
            return 'Invalid email or password'
        
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        
        conn = mysql.connect()
        cursor = conn.cursor()
        query = 'create table if not exists users (email varchar(30) primary key, name varchar(20), ' \
                'password varchar(30)) '
        cursor.execute(query)
        # print("Created ")
        
        cursor.execute("INSERT INTO users (email, name, password) VALUES (%s, %s, %s)", (email, name, password))
        conn.commit()
        
        session['email'] = email
        return redirect('/')
        
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
