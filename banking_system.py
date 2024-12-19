import sqlite3
import random
import re
from getpass import getpass

# Database Initialization
def initialize_db():
    connection = sqlite3.connect("banking_system.db")
    cursor = connection.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT UNIQUE,
            name TEXT,
            dob TEXT,
            city TEXT,
            password TEXT,
            balance REAL,
            contact_number TEXT,
            email TEXT,
            address TEXT,
            status TEXT DEFAULT 'Active'
        )
    """)

    # Transactions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT,
            type TEXT,
            amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

# Field Validators
def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def validate_contact(contact):
    return len(contact) == 10 and contact.isdigit()

def validate_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
    return re.match(pattern, password)

# Add User
# Add User Section: Debugging Password
def add_user():
    connection = sqlite3.connect("banking_system.db")
    cursor = connection.cursor()

    print("\n--- Add User ---")
    name = input("Enter name: ")
    dob = input("Enter date of birth (DD-MM-YYYY): ")
    city = input("Enter city: ")
    
    # Using input() instead of getpass() for testing
    password = input("Enter password (must include uppercase, lowercase, and number): ")

    while not validate_password(password):
        print("Invalid password. Try again.")
        password = input("Enter password (must include uppercase, lowercase, and number): ")
    
    balance = float(input("Enter initial balance (minimum 2000): "))
    while balance < 2000:
        print("Balance must be at least 2000.")
        balance = float(input("Enter initial balance: "))
    
    contact = input("Enter contact number: ")
    while not validate_contact(contact):
        print("Invalid contact number. Try again.")
        contact = input("Enter contact number: ")
    
    email = input("Enter email: ")
    while not validate_email(email):
        print("Invalid email format. Try again.")
        email = input("Enter email: ")
    
    address = input("Enter address: ")

    # Generate Unique Account Number
    account_number = str(random.randint(1000000000, 9999999999))

    # Insert User Data
    try:
        cursor.execute("""
            INSERT INTO users (account_number, name, dob, city, password, balance, contact_number, email, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (account_number, name, dob, city, password, balance, contact, email, address))
        connection.commit()
        print(f"User added successfully! Account Number: {account_number}")
    except sqlite3.IntegrityError:
        print("Failed to add user. Account number already exists.")
    
    connection.close()



# Show Users
def show_users():
    connection = sqlite3.connect("banking_system.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if users:
        print("\n--- User List ---")
        for user in users:
            print(f"""
            Account Number: {user[1]}
            Name: {user[2]}
            DOB: {user[3]}
            City: {user[4]}
            Balance: {user[6]}
            Contact: {user[7]}
            Email: {user[8]}
            Address: {user[9]}
            Status: {user[10]}
            """)
    else:
        print("No users found.")
    connection.close()

# Login and Account Operations
def login():
    connection = sqlite3.connect("banking_system.db")
    cursor = connection.cursor()

    print("\n--- Login ---")
    account_number = input("Enter account number: ").strip()
    password = input("Enter password: ").strip()

    # Fetch user data
    cursor.execute("""
        SELECT * FROM users WHERE account_number = ? AND password = ?
    """, (account_number, password))
    user = cursor.fetchone()

    if user:
        print(f"\nWelcome, {user[2]}!")  # Greet user by name
        while True:
            print("\n1. Show Balance")
            print("2. Show Transactions")
            print("3. Credit Amount")
            print("4. Debit Amount")
            print("5. Transfer Amount")
            print("6. Deactivate Account")
            print("7. Change Password")
            print("8. Update Profile")
            print("9. Logout")
            choice = input("Enter your choice (or 'b' to go back): ").strip()

            if choice == 'b':
                print("Returning to main menu.")
                break

            if choice == '1':  # Show Balance
                cursor.execute("SELECT balance FROM users WHERE account_number = ?", (account_number,))
                balance = cursor.fetchone()[0]
                print(f"Current Balance: {balance}")

            elif choice == '2':  # Show Transactions
                cursor.execute("""
                    SELECT * FROM transactions WHERE account_number = ?
                """, (account_number,))
                transactions = cursor.fetchall()
                print("\n--- Transaction History ---")
                for transaction in transactions:
                    print(f"{transaction[3]} | {transaction[2]} | Amount: {transaction[3]}")

            elif choice == '3':  # Credit Amount
                amount = float(input("Enter amount to credit: "))
                cursor.execute("UPDATE users SET balance = balance + ? WHERE account_number = ?", (amount, account_number))
                cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (?, ?, ?)", (account_number, "Credit", amount))
                connection.commit()
                print("Amount credited successfully.")

            elif choice == '4':  # Debit Amount
                amount = float(input("Enter amount to debit: "))
                cursor.execute("SELECT balance FROM users WHERE account_number = ?", (account_number,))
                balance = cursor.fetchone()[0]
                if amount > balance:
                    print("Insufficient balance.")
                else:
                    cursor.execute("UPDATE users SET balance = balance - ? WHERE account_number = ?", (amount, account_number))
                    cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (?, ?, ?)", (account_number, "Debit", amount))
                    connection.commit()
                    print("Amount debited successfully.")

            elif choice == '5':  # Transfer Amount
                target_account = input("Enter target account number: ").strip()
                amount = float(input("Enter amount to transfer: "))
                cursor.execute("SELECT balance FROM users WHERE account_number = ?", (account_number,))
                balance = cursor.fetchone()[0]
                if amount > balance:
                    print("Insufficient balance.")
                else:
                    cursor.execute("UPDATE users SET balance = balance - ? WHERE account_number = ?", (amount, account_number))
                    cursor.execute("UPDATE users SET balance = balance + ? WHERE account_number = ?", (amount, target_account))
                    cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (?, ?, ?)", (account_number, "Transfer", amount))
                    cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (?, ?, ?)", (target_account, "Received", amount))
                    connection.commit()
                    print("Amount transferred successfully.")

            elif choice == '6':  # Deactivate Account
                cursor.execute("UPDATE users SET status = 'Deactivated' WHERE account_number = ?", (account_number,))
                connection.commit()
                print("Account deactivated.")

            elif choice == '7':  # Change Password
                new_password = input("Enter new password: ")
                while not validate_password(new_password):
                    print("Invalid password. Try again.")
                    new_password = input("Enter new password: ")
                cursor.execute("UPDATE users SET password = ? WHERE account_number = ?", (new_password, account_number))
                connection.commit()
                print("Password updated successfully.")

            elif choice == '8':  # Update Profile
                new_city = input("Enter new city: ")
                new_contact = input("Enter new contact number: ")
                while not validate_contact(new_contact):
                    print("Invalid contact number. Try again.")
                    new_contact = input("Enter new contact number: ")
                new_email = input("Enter new email: ")
                while not validate_email(new_email):
                    print("Invalid email format. Try again.")
                    new_email = input("Enter new email: ")
                cursor.execute("""
                    UPDATE users SET city = ?, contact_number = ?, email = ? WHERE account_number = ?
                """, (new_city, new_contact, new_email, account_number))
                connection.commit()
                print("Profile updated successfully.")

            elif choice == '9':  # Logout
                print("Logged out.")
                break

            else:
                print("Invalid choice. Try again.")

            # Fetch the latest balance after every operation
            cursor.execute("SELECT balance FROM users WHERE account_number = ?", (account_number,))
            user = list(user)
            user[6] = cursor.fetchone()[0]  # Update the balance in the local variable

    else:
        print("Invalid account number or password.")

    connection.close()

# Main Menu
if __name__ == "__main__":
    initialize_db()
    while True:
        print("\n--- Banking System ---")
        print("1. Add User")
        print("2. Show Users")
        print("3. Login")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_user()
        elif choice == 2:
            show_users()
        elif choice == 3:
            login()
        elif choice == 4:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def view_users():
    connection = sqlite3.connect("banking_system.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("\n--- Users Table ---")
    for user in users:
        print(user)

    connection.close()

def view_transactions():
    connection = sqlite3.connect("banking_system.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    print("\n--- Transactions Table ---")
    for transaction in transactions:
        print(transaction)

    connection.close()


def debug_database():
    connection = sqlite3.connect("banking_system.db")
    cursor = connection.cursor()

    print("\n--- Debug Users Table ---")
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(row)

    print("\n--- Debug Transactions Table ---")
    cursor.execute("SELECT * FROM transactions")
    for row in cursor.fetchall():
        print(row)

    connection.close()

# Call debug_database() for debugging.

