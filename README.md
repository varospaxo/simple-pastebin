# simple-pastebin

A simple web-based PasteBin-like application built using **Flask**, **MySQL**, **Bootstrap**, and **HTML/CSS**. The app allows users to paste text, store it in a MySQL database, and view stored pastes after authentication.

## Features

- **User Authentication**: Users can sign up, log in, and manage their accounts securely.
- **Text Storage**: Paste and store text in the database.
- **Delete Options**: Delete the last paste, or clear all stored pastes with confirmation.
- **Responsive Design**: Built with Bootstrap for a mobile-friendly experience.
- **Security**: Passwords are hashed before storage.

## Tech Stack

- **Frontend**: HTML, CSS, Bootstrap
- **Backend**: Flask (Python)
- **Database**: MySQL
- **Authentication**: Flask sessions, password hashing with `werkzeug.security`

## Installation

### Prerequisites

- Python 3.x
- MySQL
- Virtual environment (`venv`) setup recommended

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/varospaxo/simple-pastebin.git
    cd pastebin-app
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate    # On Linux/MacOS
    venv\Scripts\activate       # On Windows
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a MySQL database:

  ```text
  Run the provided SQL file to create the database schema and tables.
  ```

5. Update the `db_config` in `app.py` (required) and dbgod.py (optional):

    ```python
    db_config = {
        'host': 'localhost',
        'user': 'your_mysql_user',
        'password': 'your_mysql_password',
        'database': 'pastebin_db'
    }
    ```

6. Run the application:

    ```bash
    python app.py
    ```

7. Access the application in your browser at:

    ```
    http://127.0.0.1:5000
    ```

## Routes

- `/`: Home page with text input and paste history.
- `/signup`: User registration page.
- `/login`: User login page.
- `/logout`: Logout the current user.
- `/delete_last`: Deletes the last paste entry.
- `/delete_all`: Clears all stored pastes (requires confirmation).

## Security Features

- **Password Hashing**: Passwords are stored securely using hashing (`werkzeug.security`).
- **Session Management**: Flask sessions are used to maintain user state.


