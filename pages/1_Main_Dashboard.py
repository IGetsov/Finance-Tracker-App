import streamlit as st

st.title("Main Dashboard")
def show_home():
    st.header("Home page")
    st.write("This is the main homepage")
#st.title("Role Management")

# session = next(get_db())

# roles = view_roles(session)

# for role in roles:
#     st.write(f"Role ID: {role.role_id}, Description: {role.description}")
# session.close()

