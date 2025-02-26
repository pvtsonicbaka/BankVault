import mysql.connector

class Admin:
    def __init__(self, connection):
        self.con = connection
        self.cursor = self.con.cursor(dictionary=True)

    def verify_credentials(self, admin_id, password):
        try:
            sql = "SELECT * FROM admin WHERE id = %s AND password = %s"
            self.cursor.execute(sql, (admin_id, password))
            admin = self.cursor.fetchone()
            return admin is not None
        except mysql.connector.Error as e:
            print(f"Error in verifying credentials: {e}")
            return False

    def view_all_customers(self):
        try:
            self.cursor.execute("SELECT * FROM customer")
            customers = self.cursor.fetchall()
            print("All Customers:")
            for customer in customers:
                print(customer)
        except mysql.connector.Error as e:
            print(f"Error in retrieving customers: {e}")

    def view_all_accounts(self):
        try:
            self.cursor.execute("SELECT * FROM account")
            accounts = self.cursor.fetchall()
            print("All Accounts:")
            for account in accounts:
                print(account)
        except mysql.connector.Error as e:
            print(f"Error in retrieving accounts: {e}")

    def view_all_transactions(self):
        try:
            self.cursor.execute("SELECT * FROM transaction")
            transactions = self.cursor.fetchall()
            print("All Transactions:")
            for transaction in transactions:
                print(transaction)
        except mysql.connector.Error as e:
            print(f"Error in retrieving transactions: {e}")

    def view_all_loans(self):
        try:
            self.cursor.execute("SELECT * FROM loan")
            loans = self.cursor.fetchall()
            print("All Loans:")
            for loan in loans:
                print(loan)
        except mysql.connector.Error as e:
            print(f"Error in retrieving loans: {e}")