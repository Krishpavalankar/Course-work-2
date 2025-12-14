import streamlit as st
import hashlib

st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")


# ---------- Password hashing helpers ----------
def hash_password(password: str) -> str:
    """Convert plain password to hashed password"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    """Check if entered password matches stored hash"""
    return hash_password(password) == hashed_password


# ---------- Initialise session state ----------
if "users" not in st.session_state:
    # Store users as: {username: hashed_password}
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


st.title("🔐 Welcome")


# ---------- If already logged in ----------
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to dashboard"):
        st.switch_page("pages/2_Cyber_Security.py")
    st.stop()


# ---------- Tabs: Login / Register ----------
tab_login, tab_register = st.tabs(["Login", "Register"])


# ================= LOGIN TAB =================
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in", type="primary"):
        users = st.session_state.users

        if (
            login_username in users
            and verify_password(login_password, users[login_username])
        ):
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.success(f"Welcome back, {login_username}!")

            st.switch_page("pages/2_Cyber_Security.py")
        else:
            st.error("Invalid username or password.")


# ================= REGISTER TAB =================
with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input(
        "Choose a password", type="password", key="register_password"
    )
    confirm_password = st.text_input(
        "Confirm password", type="password", key="register_confirm"
    )

    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username in st.session_state.users:
            st.error("Username already exists. Choose another one.")
        else:
            # Store HASHED password (not plain text)
            hashed_pw = hash_password(new_password)
            st.session_state.users[new_username] = hashed_pw

            st.success("Account created! You can now log in from the Login tab.")
            st.info("Tip: go to the Login tab and sign in with your new account.")
