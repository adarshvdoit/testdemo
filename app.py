from flask import Flask, render_template, request, redirect, session
from flaskext.mysql import MySQL
import uuid

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
        # conn = mysql.connect()
        # cursor = conn.cursor()
        #
        # query = 'create table if not exists books (book_id varchar(30) primary key, title  varchar(20), ' \
        #         'author  varchar(30)) , year int'
        # cursor.execute(query)

        return render_template('home.html', email=email)
    else:
        return render_template('login.html')


@app.route('/books')
def book():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookset")
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)


@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']

    conn = mysql.connect()
    cursor = conn.cursor()
    book_id = uuid.uuid4()
    cursor.execute("INSERT INTO bookset (book_id, title, author, year) VALUES (%s, %s, %s, %s)", (book_id, title, author, year))
    conn.commit()
    conn.close()

    return redirect('/books')


@app.route('/edit/<book_id>', methods=['GET', 'POST'])
def edit(book_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']

        cursor.execute("UPDATE bookset SET title = %s, author = %s, year = %s WHERE book_id = %s",
                       (title, author, year, book_id))
        conn.commit()
        conn.close()

        return redirect('/books')

    cursor.execute("SELECT * FROM bookset WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    conn.close()

    return render_template('edit.html', book=book)


@app.route('/delete/<book_id>')
def delete(book_id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bookset WHERE book_id = %s", (book_id,))
    conn.commit()
    conn.close()

    return redirect('/books')


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
