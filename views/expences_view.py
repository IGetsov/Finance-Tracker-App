from datetime import date
import streamlit as st
from services.expence_service import add_expense, get_expence_categories, get_expense_sub_categories


def display_expence_entry_menu():
    st.title("Add Expence")
    # Load expence Categories
    expense_categories = dict(get_expence_categories())
    user = st.session_state.user_object

    # Create a form for expense entry
    # with st.form("expense_form"):
    month = st.date_input("Select Month", value=date.today())
    amount = st.number_input("Amount", min_value=0.01, format="%.2f")
    category_id = st.selectbox("Expense Category", options=list(expense_categories.keys()), format_func=lambda x: expense_categories[x])
    filtered_sub_category = dict(get_expense_sub_categories(category_id))
    sub_category = st.selectbox("Select Sub Category", options=list(filtered_sub_category.keys()), format_func=lambda y: filtered_sub_category[y])
    description = st.text_area("Description", max_chars=255)

        # Submit button
    if st.button("Add Expense"):
        print(f"User: {user.user_id} // OBJ: {user}")
        
        success = add_expense(
            user_id=user.user_id, 
            month=month, 
            amount=amount, 
            category_id=category_id, 
            sub_category_id=sub_category, 
            description=description)
        if success:
            st.success("Expense added successfully!")
        else:
            st.error("Failed to add expense.")
