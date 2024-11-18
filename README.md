
# Accounting Mono

# Accounting Management System

A personal Django-based project for managing and tracking the financial accounting of my company.

## Features

- **Financial Transactions**: Record and manage income and expenses.
- **Reports**: Generate reports for cash flow, profit/loss, and other financial metrics.
- **User Management**: Basic authentication and role-based access for secure operations.
- **Scalable**: Designed with modularity in mind to allow for future enhancements.

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Vladi-bed90/acc-mono
   cd acc-mono
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
    ```
2. **Env File**
   ```bash
   DEBUG=True
   SECRET_KEY=YOUR_KEY
    ```

## Tech Stack

- **Backend**: Django
- **Frontend**: HTMX, jQuery, JavaScript, HTML/CSS
- **Database**: SQLite (default) | PostgreSQL (recommended for production)

---