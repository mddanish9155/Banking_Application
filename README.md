# Banking_Application
A comprehensive and user-friendly banking application built using Python and SQLite, offering essential banking functionalities. This project demonstrates how to build a secure, efficient, and scalable system for managing user accounts, transactions, and overall banking operations.
# Banking Application - Python & SQLite

A comprehensive and interactive banking application built with Python, leveraging SQLite as the database for lightweight and efficient data storage. This application allows you to manage user accounts, perform transactions, and maintain a transaction history with a user-friendly console-based interface.

---

## Features

### User Management
- Add new users with essential details (name, account number, balance, etc.).
- Update user information, such as contact details and email.
- Secure user authentication with password validation.
- View all registered users.

### Transactions
- Perform credit and debit transactions on user accounts.
- Transfer money between accounts securely.
- View a detailed transaction history for each user.

### Database
- **Users Table**: Stores user information like account number, balance, and personal details.
- **Transactions Table**: Logs all transactions with timestamps and transaction types.

### Validation
- Validates email formats, phone numbers, and passwords to ensure data integrity.
- Minimum initial balance requirement for account creation.

---

## Technology Stack

- **Backend**: Python (with SQLite)
- **Database**: SQLite for persistent data storage
- **Validation**: Regular Expressions for email, password, and contact validation

---

## Setup Instructions

### Prerequisites
- Python 3.x installed on your system.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/banking-application.git

### Main Menu:

  - Add users.<br>
  - View all registered users.<br>
  - Login to perform transactions.<br>
  - Exit the application.<br>
  - User Actions After Login:<br>
  - View account balance.<br>
  - Perform transactions (credit, debit, and transfers).<br>
  - View transaction history.<br>
  - Update personal details.<br>
  - Change password.<br>
  - Deactivate the account.<br>
  - Transaction History:<br>

---

#Example Interaction
### Main Menu:
--- Banking System ---
1. Add User
2. Show Users
3. Login
4. Exit
Enter your choice:
---
### After Login:
1. Show Balance
2. Show Transactions
3. Credit Amount
4. Debit Amount
5. Transfer Amount
6. Deactivate Account
7. Change Password
8. Update Profile
9. Logout
Enter your choice:
--- 

### File Structure
## /project-folder
    banking_system.py       # Main application script
    banking_system.db       # SQLite database file (auto-generated)
### Contribution
Contributions are welcome! Please fork the repository and submit a pull request with detailed comments explaining your changes.
