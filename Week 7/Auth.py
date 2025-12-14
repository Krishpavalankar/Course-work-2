USER_DATA_FILE = "users.txt"
import bcrypt
import os

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode()

def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode()
    hashed_bytes = hashed_password.encode()
    return bcrypt.checkpw(password_bytes, hashed_bytes)


test_password = "Hello123"
hashed = hash_password(test_password)

print("Original:", test_password)
print("Hashed:", hashed)
print("Correct:", verify_password(test_password, hashed))
print("Wrong:", verify_password("abc", hashed))

def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username = line.strip().split(",")[0]
            if stored_username == username:
                return True

    return False

def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    hashed = hash_password(password)

    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed}\n")

    print(f"Success: User '{username}' registered successfully!")
    return True

def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False

    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_user, stored_hash = line.strip().split(",")

            if stored_user == username:
                if verify_password(password, stored_hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False

    print("Error: Username not found.")
    return False

def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be 3–20 characters."
    if not username.isalnum():
        return False, "Username must be alphanumeric."
    return True, ""

def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    return True, ""

def display_menu():
    print("\n" + "="*50)
    print("  Secure Authentication System")
    print("="*50)
    print("[1] Register")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    print("\nWelcome to the Authentication System!")

    while True:
        display_menu()
        choice = input("Choose (1-3): ").strip()

        if choice == "1":
            print("\n--- REGISTRATION ---")
            username = input("Username: ").strip()
            valid, msg = validate_username(username)
            if not valid:
                print("Error:", msg)
                continue

            password = input("Password: ").strip()
            valid, msg = validate_password(password)
            if not valid:
                print("Error:", msg)
                continue

            confirm = input("Confirm password: ").strip()
            if confirm != password:
                print("Error: Passwords do not match.")
                continue

            register_user(username, password)

        elif choice == "2":
            print("\n--- LOGIN ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            login_user(username, password)
            input("Press Enter to continue...")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()

