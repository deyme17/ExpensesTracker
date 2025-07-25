# 💸ExpensesTracker
**ExpensesTracker** is an Android financial tracking application with Monobank API integration. It allows users to track income and expenses, analyze financial behavior, and securely manage personal budgets on the go.

## Features

- 🔐 Monobank token-based authorization
- 🔄 Automatic transaction import via secure Monobank webhook 
- ✍️ Manual creation and editing of transactions with category and description  
- 🔍 Transaction detail viewer, filtering, and sorting tools  
- 🌐 Language UI with flexible `LanguageMapper`  
- 💱 Total balance overview (per account)  
- 📊 Built-in basic financial statistics and dynamic graphs of incomes and expenses<br>
        -Line chart for dynamics over time   
        -Histogram for distribution<br>
        -Pie charts for category-wise comparison

## Architecture & Design

- 🧭 **Client-server architecture** with RESTful API  
- 🛠️ **Backend**: Flask app with PostgreSQL and main application with SQLite
- 📱 **Frontend**: Kivy mobile GUI with clean UI/UX  
- ⚙️ **Asynchronous Processing**:<br> 
          -Celery distributed task queue for webhook processing<br> 
          -Redis as message broker for reliable task delivery<br> 
          -Asynchronous data loading using `Threading`<br> 
  
- 🔐 **Security**:<br>
          - JWT-based user authentication  
          - Monobank token encryption + secure storage  
          - Password hashing using `bcrypt`
    
- 📂 **Design Patterns**:<br> 
          - **MVC** (Model-View-Controller) as the backbone of frontend logic  
          - **Repository pattern** for database abstraction  
          - **Factory pattern** for dynamic object creation (e.g., charts, services)<br>
          - **Strategy pattern** for different data processing pipelines
  
- 📦 Dockerized deployment with environment configuration  
- 📚 Extensive class and method documentation  
- 🔄 Dependency inversion principle followed for clean service injection

## Why Use It?

- ✅ Real-time statistics with minimal manual input  
- 📈 Graphical insights into spending trends  
- 🛡️ Secure, reliable, and maintainable architecture  
- 🔧 Easily extendable and testable codebase  
- 🌍 Multilingual interface for global use

## Tech Stack

- **Frontend:** Kivy (Python)  
- **Backend:** Flask  
- **Database:** PostgreSQL (and SQLite)
- **Task Queue:** Celery + Redis  
- **Auth:** JWT generation + Monobank token  
- **Containerization:** Docker

## Deploy

- The server and database are hosted on DigitalOcean (Droplet + Managed PostgreSQL).
- The domain `expenses-tracker.tech` points to the server IP.
- SSL certificates are issued via Let's Encrypt (Certbot) for secure HTTPS.
- Backend and Celery worker run in Docker containers managed with Docker Compose.