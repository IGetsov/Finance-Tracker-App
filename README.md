# Finance Tracker

Finance Tracker is a personal finance management application built with Streamlit. The app allows authenticated users to track their income by different income types and frequencies. Future features will include expense management, budget goal setting, historical data tracking, and analytical insights.

## Features

- **User Authentication**: Login, register, and logout functionalities.
- **Income Management**: Add, edit, and delete income records categorized by type (Salary, Rent, etc.) and frequency (Monthly, Daily, Yearly, etc.).
- **Database Integration**: Uses NeonDB for data persistence.
- **Custom Styling**: CSS enhancements for improved UI.
- **Planned Features**:
  - Expense tracking.
  - Budget goal setting.
  - Historical insights and analytics.

## Project Structure

```
root/
├── models/
│   ├── income_models.py         # Pydantic model for Income table
├── pages/
│   ├── Income_entry.py          # Display functions for income entry form and edit/delete menu
├── persistence/
│   ├── connectors.py            # Database connection session
│   ├── db_models.py             # ORM models corresponding to database tables
│   ├── mail_client.py           # Mail notification service
├── services/
│   ├── authentication_service.py # Handles login, register, and logout functions
│   ├── income_service.py        # Functions for creating, modifying, and deleting income records
│   ├── token_service.py         # Manages session cookies
│   ├── user_service.py          # Queries user records
├── styles/
│   ├── navbar_styles.py         # CSS custom styling for UI enhancements
├── main.py                      # Runs the main application
├── .env                          # Stores environment variables
└── requirements.txt              # Dependencies
```

## Setup and Installation

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd FinanceTracker
   ```
2. **Set up a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```sh
   streamlit run main.py
   ```

## Deployment

The app is still under development and yet to be deployed.

## Technologies Used

- **Frontend:** Streamlit
- **Backend:** Python (FastAPI, Pydantic, SQLAlchemy)
- **Database:** NeonDB
- **Authentication:** Streamlit Authenticator

## Future Enhancements

- Expense tracking
- Budget goals and alerts
- Data analytics for financial insights
- Deployment to a cloud platform

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

MIT License. See LICENSE for more details.

