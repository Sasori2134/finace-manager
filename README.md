# 💸 Finance Manager App

A powerful desktop and web-based personal finance management system built using **Django**, **Django REST Framework**, **PyQt5**, and **Sqlite**. Designed to help users track income, expenses, budgets, and get financial insights — all in one secure, user-friendly application.

## 🚀 Features

- 🔐 User authentication (JWT-based)
- ❌ JWT token blacklisting for secure logout
- 🚦 Rate limiting to prevent abuse and spam
- 💵 Track income and expenses by category
- 📊 Monthly budget planning and progress tracking
- 🔄 Manage recurring bills
- 📉 Real-time spending analytics (charts, graphs)
- 🔔 Shows when budget limits are exceeded
- 🖥️ Modern PyQt5 GUI frontend (desktop)(coming soon)
- 🌐 RESTful API backend using Django REST Framework
- 📑 Pagination

## 🛠️ Tech Stack

- **Frontend (Desktop):** PyQt5
- **Backend:** Django + Django REST Framework
- **Database:** Sqlite
- **Authentication:** JWT (JSON Web Tokens)

## 📦 Installation

### 1. Clone the Repository
```git clone https://github.com/Sasori2134/finance-manager.git```
```cd Finance_Manager```
### 2. Setup Backend
### 3. Setup Frontend

## Backend Setup
### 1. Create and activate virtual environment:
```python -m venv venvname```
```source venvname/bin/activate   # On Windows: venvname\Scripts\activate```
### 2. Install dependencies
```pip install -r requirements.txt```
### 3. Setup the database
```python manage.py makemigrations```
```python manage.py migrate```
### 3. Create superuser
```python manage.py createsuperuser```
### 4. Run the server
```python manage.py runserver```

## Frontend setup
### 1. After installing requirements go into Frontend folder
```cd Frontend```
### 2. Run main.py and enjoy the app ❤️

### API Endpoints
- 'add_transaction' - Create transaction
- 'delete_transaction/<int:pk>' - Remove transaction
- 'expenses' - Pull expenses you can filter with from_date to_date category and transaction_type
- 'register' - Registration
- 'add_budget' - Create budget
- 'delete_budget/<int:pk>' - Remove budget
- 'get_budget' - Pull budget
- 'recurring_bills' - Create recurring bills
- 'delete_recurring_bills/<int:pk>' - Remove recurring bills
- 'get_recurring_bills' - Pull created recurring bills
- 'check_recurring_bills' - check if its time to add a recurring bill (this app doesn’t use scheduling, so recurring bills are checked manually via this endpoint)
- 'api/token/' - Get JWT token
- 'api/token/refresh/' - Refresh JWT token
- 'api/log_out' - Log out (blacklist token)
- 'dashboard/monthly_average' - Pull monthly average of spendings and income for current year
- 'dashboard/monthly_data' - Pull data for graphs and charts for current year (i made it for Matplotlib, i am not sure if it works for other libraries)
- 'dashboard/total_stats' - Pull balance, total income and expense for current year
- 'dashboard/recent_transactions' - Pull 5 latest transactions
- 'dashboard/data_for_piechart_total' - Pull data for piechart grouped by category for this year
- 'analytics/analytics_data' - Pull data for graph you can pass how many days you want (in pyqt based app choices will be 30 60 90 days)
- 'analytics/analytics_stats' - Pull income average, expense average, total income and total expense you can pass how many days you want
- 'analytics/data_for_piechart_analytics' - Pull data for piechart you can pass how many days you want

Made with ❤️ by Alex (Sasori2134) — Finals Project.
Frontend made by Alex (Sasori2134)
Backend made by Alex (Sasori2134)


















