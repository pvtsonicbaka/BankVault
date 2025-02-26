import mysql.connector
import random 
from Connector import Connector
from CustomerManagement import CustomerManagement


class AccountManagement:
    def __init__(self, customer_management, connection):
        self.customer_management = customer_management
        self.con = connection
        self.cursor = self.con.cursor(dictionary=True)
        self.type = ""
        self.pin = 0

    def connect_to_db(self):
        db_connector = Connector()
        return db_connector.get_connection()

    def generate_numeric_account_id(self):
        return ''.join(str(random.randint(0, 9)) for _ in range(12))

    def generate_unique_account_id(self):
        while True:
            accno = self.generate_numeric_account_id()
            self.cursor.execute("SELECT accno FROM account WHERE accno = %s", (accno,))
            if not self.cursor.fetchone():
                return accno

    def check_balance(self):
        while True:
            balance = input("Enter Amount: ")
            if balance.isdigit():
                return float(balance)
            else:
                print("Invalid amount. Please enter a numeric value.")

    def check_pin(self):
        while True:
            pin = input("Enter PIN := ")
            if len(pin) == 4 and pin.isdigit():
                return int(pin)
            else:
                print("PIN must be a 4-digit number.")

    def check_account(self, accno):
        return accno.isdigit()

    def add_account(self):
        try:
            cid = int(input("Enter ID Number: "))
            
            # Check if the customer ID exists in the database
            self.cursor.execute("SELECT cid FROM customer WHERE cid = %s", (cid,))
            customer = self.cursor.fetchone()
            
            if customer:
                while True:
                    ch = input("1-Saving \t 2-Current: ")
                    if ch == "1":
                        self.type = "Saving"
                        break
                    elif ch == "2":
                        self.type = "Current"
                        break
                    else:
                        print("Invalid choice.")

                balance = self.check_balance()
                pin = self.check_pin()
                accno = self.generate_unique_account_id()

                sql = "INSERT INTO account (accno, cid, Balance, Type, PIN) VALUES (%s, %s, %s, %s, %s)"
                self.cursor.execute(sql, (accno, cid, balance, self.type, pin))
                self.con.commit()

                if self.cursor.rowcount > 0:
                    print("Account Added Successfully")
                else:
                    print("Failed to Add Account")
            else:
                print("ID Not Found.")
        except Exception as e:
            print(f"Error: {e}")    

    def del_account(self):
        try:
            acc = input("Enter Account Number: ")
            if self.check_account(acc):
                self.cursor.execute("SELECT PIN FROM account WHERE accno = %s", (acc,))
                account = self.cursor.fetchone()
                if account:
                    pin = self.check_pin()
                    if account['PIN'] == pin:
                        sql = "DELETE FROM account WHERE accno = %s AND PIN = %s"
                        self.cursor.execute(sql, (acc, pin))
                        self.con.commit()
                        print("Account Deleted Successfully")
                    else:
                        print("Invalid PIN")
                else:
                    print("Account Number Not Found")
            else:
                print("Invalid Account Number")
        except Exception as e:
            print(f"Error: {e}")

    def update_account_pin(self):
        try:
            acc = input("Enter Account Number: ")
            if self.check_account(acc):
                self.cursor.execute("SELECT PIN FROM account WHERE accno = %s", (acc,))
                account = self.cursor.fetchone()
                if account:
                    pin = self.check_pin()
                    if account['PIN'] == pin:
                        new_pin = self.check_pin()
                        sql = "UPDATE account SET PIN = %s WHERE accno = %s AND PIN = %s"
                        self.cursor.execute(sql, (new_pin, acc, pin))
                        self.con.commit()
                        print("PIN Updated Successfully")
                    else:
                        print("Invalid PIN")
                else:
                    print("Account Number Not Found")
            else:
                print("Invalid Account Number")
        except Exception as e:
            print(f"Error: {e}")

    def view_balance(self):
        try:
            accno = input("Enter Account Number: ")
            if self.check_account(accno):
                pin = self.check_pin()
                self.cursor.execute("SELECT Balance FROM account WHERE accno = %s AND PIN = %s", (accno, pin))
                account = self.cursor.fetchone()
                if account:
                    print(f"Account Number: {accno}")
                    print(f"Balance: {account['Balance']}")
                else:
                    print("Incorrect Account Number or PIN")
            else:
                print("Invalid Account Number")
        except Exception as e:
            print(f"Error: {e}")
