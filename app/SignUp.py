import streamlit as st
import bcrypt
# // converts string to non readable string

def create_sign_up_page(update_session):
    # Header and Subheader
    st.title("🔒 Create an Account ")
    st.subheader("Join us and get started today!")
    
    # Create input fields for username, password, email, and phone
    username = st.text_input("Username")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
   
    # Create a sign-up button
    if st.button("Sign Up"):
        if username and email and phone and password and confirm_password:
            if password == confirm_password:
                # Hash the password using bcrypt
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                # Store the user data with the hashed password
                st.session_state.users.append({
                    "username": username,
                    "email": email,
                    "phone_number": phone,
                    "password": hashed_password.decode('utf-8'),  # Convert bytes to string
                })

                update_session("users", st.session_state.users)  # Now update session
                st.success("Account created successfully!")
            else:
                st.error("Passwords do not match.")
        else:
            st.error("Please fill in all fields.")
            
    
    # Sign Up Link
    st.markdown(f"""
    <div style="text-align: center; margin-top: 20px;">
        <div>User count: {len(st.session_state.users)} </div> 
        Already have an account? <a href="/?page=Login" target="_self">Login here</a>.
    </div>
    """, unsafe_allow_html=True)

