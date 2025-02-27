from datetime import date
import streamlit as st
from services.income_service import add_income, delete_income, edit_income, get_frequencies, get_income_categories, get_user_incomes
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
        user = view_user_by_name(username) 
        if not user:
            st.error("User not found! Please login again.")
            return 

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Save Income"):
                if not month:
                    month = date.today()
                if amount <= 0:
                    st.error("Please enter a valid income amount!")
                    return

                try:
                    income = add_income(user.user_id, amount, income_type_id, income_frequency_id)
                    st.success(f"Income {income} added successfully! 🎉")
                except Exception as e:
                    st.error(f"Error: {e}")

        with col2:
            if st.button("View My Incomes"):
                display_user_income_menu(user.user_id, income_categories, frequencies)


def display_user_income_menu(user_id, income_categories, frequencies):
    st.subheader("Your Income Records")
    user_incomes = get_user_incomes(user_id)

    if user_incomes:
        # Convert to a displayable table format
        import pandas as pd
        income_df = []
        for income in user_incomes:
            income_df.append({
                "ID": income.id,
                "Amount ($)": income.amount_encrypted,
                "Type": income_categories.get(income.income_type_id, "Unknown"),
                "Frequency": frequencies.get(income.income_frequency_id, "Unknown"),
                "Month": income.month.strftime("%Y-%m")
            })

        df = pd.DataFrame(income_df)
        selected_row = st.selectbox("Select an income to edit/delete:", df.index)
        selected_income = user_incomes[selected_row]

        # Form fields for editing
        month = st.date_input("Month:", value=selected_income.month)
        amount = st.number_input("Income Amount ($):", min_value=0.0, value=float(selected_income.amount_encrypted), format="%.2f")
        income_type_id = st.selectbox("Income Type:", options=list(income_categories.keys()), index=list(income_categories.keys()).index(selected_income.income_type_id), format_func=lambda x: income_categories[x])
        income_frequency_id = st.selectbox("Income Frequency:", options=list(frequencies.keys()), index=list(frequencies.keys()).index(selected_income.income_frequency_id), format_func=lambda x: frequencies[x])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Update Income"):
                try:
                    edit_income(selected_income.id, user_id, amount, income_type_id, income_frequency_id, month)
                    st.success("Income updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating income: {e}")

        with col2:
            if st.button("Delete Income", type="primary"):
                try:
                    delete_income(selected_income.id, user_id)
                    st.success("Income deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting income: {e}")
