# Library Management System

A command-line Library Management System built with Python and MySQL. 
Supports book management, issuing/returning books, and admin-authenticated 
access through a simple menu-driven interface.

## Features

- Admin login authentication
- Add and delete books
- Issue books to students with availability tracking
- Return books with validation (prevents falsely marking unissued books as returned)
- View all books, issued books, or search by title
- Parameterized SQL queries (protected against SQL injection)
- Error handling for invalid input and duplicate entries

## Tech Stack

- **Python** — application logic and CLI interface
- **MySQL** — relational data storage
- **mysql-connector-python** — database connectivity

## Database Schema

Two tables linked by a foreign key:
- `books` — book ID, title, author, availability status
- `issue_details` — tracks which books are issued to which students, 
  referencing `books.b_id`
  
## How to Run

1. Install dependencies:
   pip install mysql-connector-python
2. Make sure MySQL is running locally, and update the `password` field in 
   the script to match your MySQL root password.
3. Run the script:
   python library_management_system.py
4. Log in with:
   - Username: `admin`
   - Password: `library123`

## Status

Built as a personal exercise in integrating Python with a relational database.

## How to Run

1. Install dependencies:
