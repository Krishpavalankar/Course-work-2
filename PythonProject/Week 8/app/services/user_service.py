import bcrypt
from pathlib import Path
from app.data.users import get_user_by_username, insert_user
import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user

DATA_DIR = Path("DATA")


# -----------------------------------------------------
# REGISTER USER
# -----------------------------------------------------
def register_user(username, password, role="user"):
    conn = connect_database()
    cursor = conn.cursor()

    # Check if exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."

    # Hash
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    insert_user(username, password_hash, role)

    conn.close()
    return True, f"User '{username}' registered successfully."


# -----------------------------------------------------
# LOGIN USER
# -----------------------------------------------------
def login_user(username, password):
    user = get_user_by_username(username)

    if not user:
        return False, "User not found."

    stored_hash = user[2].encode()

    if bcrypt.checkpw(password.encode(), stored_hash):
        return True, "Login successful!"
    else:
        return False, "Incorrect password."


# -----------------------------------------------------
# MIGRATE USERS FROM users.txt
# -----------------------------------------------------
def migrate_users_from_file(conn=None, filepath=DATA_DIR / "users.txt"):
    """
    Reads users.txt and inserts usernames + password hashes into DB.
    """
    if conn is None:
        conn = connect_database()

    if not filepath.exists():
        print
