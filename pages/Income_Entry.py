from datetime import date
import streamlit as st
from services.income_service import add_income, get_frequencies, get_income_categories
from services.token_service import get_authenticator
from services.user_service import view_user_by_name 

authenticator, _ = get_authenticator()

def display_income_entry_menu():
    st.title("Enter your income 💰")

    # Load categories and frequencies from the database
    income_categories = dict(get_income_categories())
    frequencies = dict(get_frequencies())


    # User input fields
    month = st.date_input("Month (Optional):", value=None)
    amount = st.number_input("Income Amount ($):", min_value=0.0, format="%.2f")
    income_type_id = st.selectbox("Income Type:", options=list(income_categories.keys()), format_func=lambda x: income_categories[x])
    income_frequency_id = st.selectbox("Income Frequency:", options=list(frequencies.keys()), format_func=lambda x: frequencies[x])

    # Tooltip for guidance
    st.info("💡 Select the income type and frequency from the dropdown lists.")

    # Get user credentials
    name, authentication_status, username = authenticator.login("Login", location="main")

    # show Submit button if user is authenticated
    if authentication_status: 
        if st.button("Save Income"):
            if not month:
                month = date.today()
            if amount <= 0:
                st.error("Please a valid income amount!")
                return
            
            user = view_user_by_name(username)
            if not user:
                st.error("User was not found! Please login")
            
            try:
                income = add_income(user.user_id, amount, income_type_id, income_frequency_id)
                print(income)
                st.success(f"Income {income} added successfully! 🎉")
            except Exception as e:
                st.error(f"Error: {e}")
