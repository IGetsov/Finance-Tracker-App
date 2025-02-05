from datetime import date
import streamlit as st
from services.income_service import get_frequencies, get_income_categories


st.title("Income Entry Form 💰")

# Load categories and frequencies from the database
categories = get_income_categories()
print(f'This IS THE OUTPUT {categories}')
income_categories = dict(get_income_categories())

#frequencies = dict(get_frequencies())

# User input fields
month = st.date_input("Month (Optional):", value=None)
amount = st.number_input("Income Amount ($):", min_value=0.0, format="%.2f")
income_type_id = st.selectbox("Income Type:", options=list(income_categories.keys()), format_func=lambda x: income_categories[x])
#income_frequency_id = st.selectbox("Income Frequency:", options=list(frequencies.keys()), format_func=lambda x: frequencies[x])

# Tooltip for guidance
st.info("💡 Select the income type and frequency from the dropdown lists.")

# Submit button
if st.button("Save Income"):
    if not month:
        month = date.today()
    if amount <= 0:
        st.error("Please a valid income amount!")
    
    try:
        st.success("Income added successfully! 🎉")
    except Exception as e:
        st.error(f"Error: {e}")
