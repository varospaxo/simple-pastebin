import mysql.connector
from werkzeug.security import generate_password_hash

# MySQL database configuration
db_config = {
    'host': 'localhost', # Replace with your MySQL hostname
    'user': 'root', # Replace with your MySQL username
    'password': 'root',  # Replace with your MySQL password
    'database': 'pastebin_db'
}

def connect_db():
    """Establish a database connection and return the cursor and connection."""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    return conn, cursor

def add_user(username, password):
    """Add a new user to the database."""
    conn, cursor = connect_db()

    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        print(f"Error: User '{username}' already exists!")
    else:
        hashed_password = generate_password_hash(password)  # Assuming you have a hash_password function
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            print(f"User '{username}' added successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    cursor.close()
    conn.close()

def view_users():
    """View all users and their passwords in the database."""
    conn, cursor = connect_db()

    cursor.execute("SELECT id, username, password FROM users")
    users = cursor.fetchall()

    if users:
        print("\nList of users with passwords:")
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Password: {user[2]}")
    else:
        print("No users found.")

    cursor.close()
    conn.close()

def delete_user(username):
    """Delete a user from the database."""
    conn, cursor = connect_db()

    try:
        cursor.execute("DELETE FROM pastes WHERE username = %s", (username,))
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"User '{username}' deleted successfully!")
        else:
            print(f"User '{username}' not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def view_pastes():
    """View all pastes along with the usernames of the users who made them."""
    conn, cursor = connect_db()

    # Query to fetch pastes along with the username of the user who made them
    query = """SELECT * FROM pastes;"""
    cursor.execute(query)
    pastes = cursor.fetchall()

    if pastes:
        print("\nList of all pastes with usernames:")
        for paste in pastes:
            print(f"ID: {paste[0]}, Content: {paste[1]}, User: {paste[2]}, Created At: {paste[3]}")
    else:
        print("No pastes found.")

    cursor.close()
    conn.close()

def menu():
    """Display a menu and handle user choices."""
    while True:
        print("\n--- User Management Menu ---")
        print("1. Create a new user")
        print("2. View all users (with hashed passwords)")
        print("3. Delete a user")
        print("4. View all pastes with usernames")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            add_user(username, password)
        elif choice == '2':
            view_users()
        elif choice == '3':
            username = input("Enter username to delete: ")
            delete_user(username)
        elif choice == '4':
            view_pastes()
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == '__main__':
    menu()