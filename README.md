# Help Desk Ticket Management System

## Overview

This project is a web-based Help Desk Ticket Management System developed using Python, Flask, SQLAlchemy, and SQLite. The application allows users to register, log in, create support tickets, view existing tickets, and update ticket information. Administrative users have additional permissions to manage application data.

---

## Technologies Used

* Python 3.x
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-WTF
* WTForms
* SQLite
* HTML5
* CSS3

---

## Project Structure

```text
Project/
│
├── instance/
│   └── database.db
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── tickets.html
│   ├── create_ticket.html
│   ├── edit_ticket.html
│
├── app.py
├── config.py
├── extensions.py
├── forms.py
├── models.py
├── requirements.txt
└── README.md
```

---

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd project-folder
```

### Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask development server:

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

## Database

The application uses SQLite.

When the application starts for the first time:

* Database tables are automatically created.
* Sample data is automatically seeded if the database is empty.
* Two administrator accounts and eight standard user accounts are created.

---

## Sample Login Accounts

### Administrator

Username: admin1

Password: Password123

### Standard User

Username: user1

Password: Password123

---

## Features

* User registration
* User authentication
* Role-based access control
* Ticket creation
* Ticket viewing
* Ticket editing
* Ticket deletion (administrators only)
* Form validation
* Flash notifications
* SQLite database integration

---

## Deployment to Render

### Create a Render Account

Create a free account at Render.

### Create a New Web Service

Connect the GitHub repository containing the application.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app:app
```

### Environment Variables

Configure:

```text
SECRET_KEY=<your-secret-key>
```

### Deploy

Render will automatically build and deploy the application.

Once deployment completes, Render will provide a public URL that can be used to access the application.

---

## Author

Developed as part of a university Web Development Project assignment.
