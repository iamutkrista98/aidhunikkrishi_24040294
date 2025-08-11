import streamlit as st
import bcrypt


def create_login_page(update_session):
    # Header and Subheader
    st.title("🔑 Welcome Back!")
    st.subheader("Enter your credentials to continue.")


    # Login Form
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        remember_me = st.checkbox("Remember me")
        login_button = st.form_submit_button("Login")

        if login_button:
            if email and password:  # Basic validation
                # Check if the user exists in the session state
                user_found = False
                user = None
                for usr in st.session_state.users:
                    if usr["email"] == email and bcrypt.checkpw(password.encode('utf-8'), usr["password"].encode('utf-8')):
                        user_found = True
                        user = usr
                        break

                if user_found:
                    st.success("Logged in successfully!")
                    update_session('isLoggedIn', True)
                    update_session('user', user)
                    st.query_params["page"] = 'Home'
                    return
                else:
                    st.error("Invalid email or password. Please try again.")
            else:
                st.error("Please fill in all fields.")

    # Sign Up Link
    st.markdown(f"""
    <div style="text-align: center; margin-top: 20px;">
        <div>User count: {len(st.session_state.users)} </div> 
        Don't have an account? <a href="?page=Sign+Up" target="_self">Sign up here</a>.
    </div>
    """, unsafe_allow_html=True)