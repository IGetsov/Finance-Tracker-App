import streamlit as st
import streamlit_authenticator as stauth
from services import user_service as us
from pages import Income_Entry as ie
from services.token_service import get_authenticator
from pages import Income_Entry as ie
from views.expences_view import display_expence_entry_menu


authenticator, config = get_authenticator()

st.title("Finance Tracker Dashboard")

st.write("Money Management Made Easy")

# Initialize session state for managing content display
if "selected_section" not in st.session_state:
    st.session_state.selected_section = None
    st.session_state.toggle_element = True

# Toggle between Login and Register
#choice = st.radio("Select an option:", ["Login", "Register"])
show_login = True

# Toggle between Login and Register
if st.session_state.toggle_element:
    if st.toggle("Login/Register", show_login):
        show_login = True
    else:
        show_login = False


if show_login:
    name, authentication_status, username = authenticator.login("Login", location="main")
    

    # Handle login cases
    if authentication_status:
        # print(f'{username} password: {config["credentials"]["usernames"][username]["password"]}')
        login_response = us.login_user(username, config["credentials"]["usernames"][username]["password"])
        
        # Logout button
        if authenticator.logout("Logout", "main"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
                
            # Clear Streamlit cache
            st.session_state.clear()
            st.cache_data.clear()
            st.rerun()
     

        st.sidebar.write(f"Welcome, {username}!")
        st.session_state.toggle_element = False
        st.session_state.user_object = us.view_user_by_name(username)

        # Display user control buttons
        st.subheader("Manage your finances")
        col1, col2, col3 = st.columns(3)
        # Render Manage Income menu
        with col1:
            if st.button("Manage Income", key="income_add"):
                st.session_state.selected_section = "income"
            if st.button("View My Incomes", key="income_view"):
                st.session_state.selected_section = "income_history"
        # Renger Manage Expceces menu
        with col2:
            if st.button("Manage Expences", key="expence_add"):
                st.session_state.selected_section = "expence"
        # Render Manage Goals menu
        with col3:
            if st.button("Manage Goals", key="goal_add"):
                st.session_state.selected_section = "goals"
        # Add divider after the buttons
        st.divider()

        if st.session_state.selected_section == "income":
            ie.display_income_entry_menu()
   
        elif st.session_state.selected_section == "income_history":
            usr_id = st.session_state.user_object.user_id
            ie.display_user_income_menu(usr_id)
        elif st.session_state.selected_section == "expence":
            display_expence_entry_menu()
        elif st.session_state.selected_section == "goals":
            st.warning("Not implemented yet!")

    elif authentication_status is False:
        st.error("Invalid username or password")

    elif authentication_status is None:
        st.warning("Please enter your username and password")

else:
    st.subheader("Register a new account")

    new_username = st.text_input("Username")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Password", type="password", key="confirm_register_password")

    if st.button("Register"):
        if new_username in config["credentials"]["usernames"]:
            st.error("Username already exists. Choose another one.")
        elif new_password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Generate JWT token as password placeholder
            hashed_password = stauth.Hasher([new_password]).generate()[0]

            us.register_user(new_username, new_email, hashed_password)

            st.success("Registration successful! You can now log in.")



# if __name__ == "__main__":
#     st.rerun

