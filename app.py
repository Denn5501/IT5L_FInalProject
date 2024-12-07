from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change for production security

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))  # Redirect to homepage after successful login
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))

    return render_template('login.html')

# Route for homepage
@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    cars = [
        {"name": "Toyota AE86 Trueno", "price": "$50/day", "image": "trueno.jpg"},
        {"name": "Nissan Skyline R32", "price": "$80/day", "image": "skyline_r32.jpg"},
        {"name": "Mazda RX-7", "price": "$100/day", "image": "mazda_rx7.jpg"},
        {"name": "Nissan S13 Silvia", "price": "$100/day", "image": "nissan_silvia_s13.jpg"}
    ]
    return render_template('index.html', cars=cars, username=session.get('username'))

# Route for logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        # Check if the username already exists
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user:
            flash("Username already exists.")
            return redirect(url_for('register'))

        # Add new user to the database
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
