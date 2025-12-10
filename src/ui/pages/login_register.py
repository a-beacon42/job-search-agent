import streamlit as st
from services.login_register.register import (
    RegistrationService,
    UserRegistrationRequest,
)
from services.login_register.login import LoginService
from core.repositories import UserRepo
from core.db import get_session

db = get_session()
user_repo = UserRepo(db)
reg_service = RegistrationService(user_repository=user_repo)
login_service = LoginService(user_repository=user_repo)

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

tabs = st.tabs(["Login", "Register"])
# todo - convert both to st.form

with tabs[0]:
    st.header("Login")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")
    if st.button("Sign in"):
        if login_email and login_password:
            user = login_service.login_user(login_email, login_password)
            st.info(f"found {user}")
            if user:
                st.session_state["user_id"] = user.id
                st.success(f"Welcome back, {login_email}!")
                st.query_params["user_id"] = str(user.id)
                st.switch_page(page="pages/home.py")
            else:
                st.error("Invalid email or password.")
        else:
            st.error("Please enter both email and password.")

with tabs[1]:
    st.header("Register")
    col1, col2 = st.columns(2)
    with col1:
        f_name = st.text_input("First Name", key="first_name")
    with col2:
        l_name = st.text_input("Last Name", key="last_name")
    reg_email = st.text_input("Email", key="register_email")
    reg_password = st.text_input("Password", type="password", key="register_password")
    reg_confirm = st.text_input(
        "Confirm Password", type="password", key="register_confirm"
    )
    agree_terms = st.checkbox("I agree to the Terms of Service", key="register_terms")

    if st.button("Create account"):
        if not all([reg_email, reg_password, reg_confirm]):
            st.error("Fill in all fields.")
        elif reg_password != reg_confirm:
            st.error("Passwords do not match.")
        elif not agree_terms:
            st.error("Please agree to the Terms of Service.")
        else:
            try:
                new_user_req = UserRegistrationRequest(
                    email=reg_email,
                    password=reg_password,
                    first_name=f_name,
                    last_name=l_name,
                )
                try:
                    result = reg_service.register_user(new_user_req)
                    if not result.success:
                        st.error(f"Registration failed: {result.message}")
                    else:
                        st.success(
                            f"Account created for {reg_email}. You can now log in."
                        )
                        st.session_state["user_id"] = result.user_id
                        st.query_params["user_id"] = str(result.user_id)
                        st.switch_page(page="pages/home.py")
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")
                finally:
                    db.close()
            except Exception as e:
                st.error(f"Error creating registration request: {str(e)}")
