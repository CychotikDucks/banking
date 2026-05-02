import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        balance REAL DEFAULT 0.0
    )
''')


cursor.execute('''
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        type TEXT,
        amount REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_id) REFERENCES accounts(id)
    )
''')

conn.commit()
print("Database created successfully!")
print("Tables: accounts, transactions")


def create_account(name, initial_deposit=0.0):
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, initial_deposit))
    conn.commit()
    account_id = cursor.lastrowid
    if initial_deposit > 0:
        cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)", (account_id, initial_deposit))
        conn.commit()
    print(f"Account created for {name} (ID: {account_id}) with balance ${initial_deposit:.2f}")
    return account_id

def deposit(account_id, amount):
    if amount <= 0:
        print("Error: Deposit amount must be positive.")
        return
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)", (account_id, amount))
    conn.commit()
    balance = check_balance(account_id)
    print(f"Deposited ${amount:.2f}. New balance: ${balance:.2f}")

def withdraw(account_id, amount):
    if amount <= 0:
        print("Error: Withdrawal amount must be positive.")
        return
    balance = check_balance(account_id)
    if amount > balance:
        print(f"Error: Insufficient funds. Balance: ${balance:.2f}, Requested: ${amount:.2f}")
        return
    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'withdrawal', ?)", (account_id, amount))
    conn.commit()
    new_balance = check_balance(account_id)
    print(f"Withdrew ${amount:.2f}. New balance: ${new_balance:.2f}")

def check_balance(account_id):
    cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    row = cursor.fetchone()
    if row is None:
        print(f"Error: Account {account_id} not found, please try again.")
        return 0.0
    else:
        return row[0]


def main_menu():
    end = False
    while end == False:    
        print("\n=== Shawn Banking ===")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Exit")

        choice = input("Choose an option: ")
     
        if choice == "1":
            name = input("Enter account holder first and last name: ")
            amount = float(input("Initial deposit amount: "))
            create_account(name, amount)
        elif choice == "2":
            acc_id = int(input("Account ID: "))
            amount = float(input("Deposit amount: "))
            deposit(acc_id, amount)
        elif choice == "3":
            acc_id = int(input("Account ID: "))
            amount = float(input("Withdrawal amount: "))
            withdraw(acc_id, amount)
        elif choice == "4":
            acc_id = int(input("Account ID: "))
            balance = check_balance(acc_id)
            print(f"Balance: ${balance:.2f}")
        elif choice == "5":
            print("Thank you for using Shawn Banking! Hope to see you again! ")
            end = True
        else:
            print("Invalid option. Try again.")


main_menu()
# Always close when done
conn.close()