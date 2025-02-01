import streamlit as st
from services.user_service import view_roles
from persistence.connectors import get_db

st.title("Role Management")

session = next(get_db())
roles = view_roles(session)

for role in roles:
    st.write(f"Role ID: {role.role_id}, Description: {role.description}")
session.close()