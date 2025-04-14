from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL configuration
db_config = {
    'host': 'localhost', # Replace with your MySQL hostname
    'user': 'root', # Replace with your MySQL username
    'password': 'root',  # Replace with your MySQL password
    'database': 'pastebin_db'
}
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Check if the username already exists
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already taken, please choose another one.', 'danger')
            return redirect(url_for('signup'))

        # Add the new user to the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Account created successfully! You can now log in.', 'success')
        
        # return redirect(url_for('login'))

    return render_template('signup.html')

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[0], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials, please try again.", "danger")

    return render_template('login.html')

# Main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if request.method == 'POST':
        content = request.form['content']
        cursor.execute("INSERT INTO pastes (content, username) VALUES (%s, %s)", (content, username))
        conn.commit()

    # Get sort order from the query parameter, default to DESC (newest first)
    sort_order = request.args.get('sort', 'DESC')
    
    # Validate sort_order to prevent SQL injection
    if sort_order not in ['ASC', 'DESC']:
        sort_order = 'DESC'  # Default to DESC if invalid value is provided
    
    # Use parameterized query with validated sort_order
    query = f"SELECT id, content, created_at FROM pastes WHERE username=%s ORDER BY created_at {sort_order}"
    cursor.execute(query, (username,))
    pastes = cursor.fetchall()
    conn.close()

    return render_template('index.html', pastes=pastes, username=username, current_sort=sort_order)

# Route to delete a specific paste
@app.route('/delete_paste/<int:paste_id>', methods=['POST'])
def delete_paste(paste_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Ensure the paste belongs to the current user before deleting
    cursor.execute("DELETE FROM pastes WHERE id=%s AND username=%s", (paste_id, session['username']))
    conn.commit()
    conn.close()

    flash("Paste deleted successfully!", "success")
    
    # Get sort order from the query parameter, default to DESC (newest first)
    sort_order = request.args.get('sort', 'DESC')
    
    # Validate sort_order to prevent SQL injection
    if sort_order not in ['ASC', 'DESC']:
        sort_order = 'DESC'  # Default to DESC if invalid value is provided
    
    return redirect(url_for('index', sort=sort_order))

# Route to delete all records
@app.route('/delete_all', methods=['POST'])
def delete_all():
    if 'username' not in session:
        return redirect(url_for('login'))

    confirmation = request.form.get('confirmation')
    if confirmation != 'CONFIRM':
        flash("Please type 'CONFIRM' to delete all records.", "danger")
        return redirect(url_for('index'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM pastes WHERE username=%s", (session['username'],))
    conn.commit()
    conn.close()

    flash("All pastes deleted successfully!", "success")
    return redirect(url_for('index'))

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)