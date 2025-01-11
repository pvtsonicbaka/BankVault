import mysql.connector
import random
import Connector

class AccountManagement:
    def __init__(self):
        self.con = self.connect_to_db()
        self.cursor = self.con.cursor(dictionary=True)
        self.acc_balance = {}
        self.hsacc = {}
        self.type = ""
        self.pin = 0

    def connect_to_db(self):
        db_connector = Connector()
        return db_connector.get_connection()

    def generate_numeric_account_id(self):
        return ''.join(str(random.randint(0, 9)) for _ in range(12))

    def check_balance(self):
        while True:
            try:
                balance = input("Enter Amount: ")
                if balance.isdigit():
                    return float(balance)
                else:
                    print("Invalid amount. Please enter a numeric value.")
            except ValueError:
                print("Invalid input.")

    def check_pin(self):
        while True:
            pin = input("Enter PIN: ")
            if len(pin) == 4 and pin.isdigit():
                return int(pin)
            else:
                print("PIN must be a 4-digit number.")

    def check_account(self, accno):
        return accno.isdigit()

    def get_acc_id(self):
        self.hsacc.clear()
        self.cursor.execute("SELECT * FROM account")
        for row in self.cursor.fetchall():
            self.hsacc[row['accno']] = row['PIN']

    def set_balance(self):
        self.acc_balance.clear()
        self.cursor.execute("SELECT * FROM account")
        for row in self.cursor.fetchall():
            self.acc_balance[row['accno']] = row['Balance']

    def add_account(self):
        try:
            self.get_acc_id()
            cid = int(input("Enter ID Number: "))
            if cid in CustomerManagement.hscid:  # Assuming `CustomerManagement.hscid` is a valid set/dict
                while True:
                    ch = int(input("1-Saving \t 2-Current: "))
                    if ch == 1:
                        self.type = "Saving"
                        break
                    elif ch == 2:
                        self.type = "Current"
                        break
                    else:
                        print("Invalid choice.")
                
                balance = self.check_balance()
                pin = self.check_pin()
                accno = self.generate_numeric_account_id()
                sql = "INSERT INTO account (accno, c_id, Balance, Type, PIN) VALUES (%s, %s, %s, %s, %s)"
                self.cursor.execute(sql, (accno, cid, balance, self.type, pin))
                self.con.commit()
                print("Account Added Successfully")
            else:
                print("ID Not Found.")
        except Exception as e:
            print(f"Error: {e}")

    def del_account(self):
        try:
            self.get_acc_id()
            acc = input("Enter Account Number: ")
            if self.check_account(acc):
                if acc in self.hsacc:
                    pin = self.check_pin()
                    if self.hsacc[acc] == pin:
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
            self.get_acc_id()
            acc = input("Enter Account Number: ")
            if self.check_account(acc):
                if acc in self.hsacc:
                    pin = self.check_pin()
                    if self.hsacc[acc] == pin:
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
            self.set_balance()
            self.get_acc_id()
            accno = input("Enter Account Number: ")
            if self.check_account(accno):
                pin = self.check_pin()
                if self.hsacc.get(accno) == pin:
                    if accno in self.acc_balance:
                        print(f"Account Number: {accno}")
                        print(f"Balance: {self.acc_balance[accno]}")
                    else:
                        print("Account Number Not Found")
                else:
                    print("Incorrect PIN")
            else:
                print("Invalid Account Number")
        except Exception as e:
            print(f"Error: {e}")


