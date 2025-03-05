from datetime import date, datetime
import streamlit as st
from services.income_service import add_income, delete_income, edit_income, get_frequencies, get_income_categories, get_user_incomes
from services.token_service import get_authenticator
from services.user_service import view_user_by_name 
import pandas as pd

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
            if st.button("Go back"):
                st.write("Function not applied yet")


def display_user_income_menu(user_id):
    st.subheader("Your Income Records")
    # Get Income records for user_id
    user_incomes = get_user_incomes(user_id)
    # Get all category types and reference them via object ID
    categories = get_income_categories()
    # Get all frequencies and reference them via object ID
    frequencies = get_frequencies()

    if user_incomes:
        # Convert to a displayable table format
        income_df = []
        for income in user_incomes:
            income_df.append({
                "ID": income.income_id,
                "Amount ($)": float(income.amount_encrypted),
                "Type": categories.get(income.income_type_id, "Unknown"),
                "Frequency": frequencies.get(income.income_frequency_id, "Unknown"),
                "Month": income.month.strftime("%Y-%m")
            })

        df = pd.DataFrame(income_df)

        selection = dataframe_with_selections(df)
        st.write(selection)

        if not selection.empty:
            st.info(f"Editing {len(selection)} record(s)")

            for _, row in selection.iterrows():
                print(f"ROW DATA:: {row}")
                with st.form(f"edit_form_{row['ID']}"):
                    st.subheader(f"Edit Income ID {row['ID']}")

                    try:
                        amount_value = float(row["Amount ($)"])  
                    except ValueError:
                        amount_value = 0.0  

                    new_amount = st.number_input(
                        "Amount ($)", value=amount_value, min_value=0.01  
                    )
                    income_type_id = next((k for k, v in categories.items() if v == row["Type"]), None)

                    new_income_type = st.selectbox(
                        "Income Type",
                        options=list(categories.keys()), 
                        format_func=lambda x: categories[x], 
                        index=list(categories.keys()).index(income_type_id) if income_type_id else 0
                    )

                    frequency_id = next((k for k, v in frequencies.items() if v == row["Frequency"]), None)

                    new_frequency = st.selectbox(
                        "Frequency",
                        options=list(frequencies.keys()),  
                        format_func=lambda x: frequencies[x],  
                        index=list(frequencies.keys()).index(frequency_id) if frequency_id else 0
                    )

                    new_month = st.date_input("Month", value=datetime.strptime(row["Month"], "%Y-%m").date())

                    if st.form_submit_button("Save Changes"):
                        edit_income(
                            income_id=row["ID"],
                            user_id=user_id,
                            amount=new_amount,
                            income_type=new_income_type,
                            frequency=new_frequency,
                            month=new_month
                        )
                        st.success(f"Income ID {row['ID']} updated successfully!")
                        st.rerun()

                # Delete Button (outside form)
                if st.button(f"Delete {row['ID']}", key=f"delete_{row['ID']}"):
                    delete_income(row["ID"], user_id)
                    st.success(f"Income record {row['ID']} deleted!")
                    st.rerun()


def dataframe_with_selections(df: pd.DataFrame, init_value: bool = False) -> pd.DataFrame:
    """Helper function that adds selection column to a DataFrame and generates selection table below it."""
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", init_value)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)