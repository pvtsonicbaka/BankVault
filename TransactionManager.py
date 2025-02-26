import random
import os
from datetime import datetime
import mysql.connector
from AccountManagement import AccountManagement
from Connector import Connector

class TransactionManager:
    def __init__(self, customer_management, connection):
        self.am = AccountManagement(customer_management, connection)
        print("Trans")
        self.sc = input
        self.pin = None
        self.to_cid = None
        self.from_cid = None
        self.DateOfTransaction = None
        self.balance = None
        self.amount = None
        self.acc_no = None
        self.con = connection
        self.cursor = self.con.cursor(dictionary=True)
        self.ps = None

    def login(self):
        acc = input("Enter Account Number: ")
        if self.am.check_account(acc):
            self.cursor.execute("SELECT PIN FROM account WHERE accno = %s", (acc,))
            account = self.cursor.fetchone()
            if account:
                self.pin = self.am.check_pin()
                if account['PIN'] == self.pin:
                    return acc
                else:
                    print("Invalid PIN")
            else:
                print("Account Number Not Found")
        else:
            print("Invalid Account Number")
        return None

    def with_draw(self):
        acc = self.login()
        if acc:
            try:
                self.cursor.execute("SELECT Balance FROM account WHERE accno = %s", (acc,))
                account = self.cursor.fetchone()
                if account:
                    print("Set Amount to Withdraw")
                    self.amount = self.am.check_balance()
                    balance = account['Balance']
                    if balance >= self.amount:
                        new_balance = balance - self.amount
                        sql = "UPDATE account SET Balance=%s WHERE accno=%s"
                        self.ps = self.con.cursor()
                        self.ps.execute(sql, (new_balance, acc))
                        if self.ps.rowcount > 0:
                            formatted_date = datetime.now().strftime("%Y-%m-%d")
                            transaction_id = self.generate_transaction_id()
                            sql = "INSERT INTO transaction (transaction_ID, from_accNo, to_accNo, amount, Date) VALUES (%s, %s, %s, %s, %s)"
                            self.ps.execute(sql, (transaction_id, acc, acc, -self.amount, formatted_date))
                            if self.ps.rowcount > 0:
                                self.con.commit() 
                                print(f"Rs:- {self.amount}/- Is Withdrawn Successfully")
                                print("Transaction recorded successfully")
                            else:
                                self.con.rollback()
                                print("Failed to record transaction")
                        else:
                            self.con.rollback()
                            print("Payment failed")
                    else:
                        print("Insufficient Balance to Withdraw")
            except mysql.connector.Error as e:
                self.con.rollback()
                print(f"An error occurred: {e}")

    def deposit(self):
        acc = self.login()
        if acc:
            try:
                self.cursor.execute("SELECT Balance FROM account WHERE accno = %s", (acc,))
                account = self.cursor.fetchone()
                if account:
                    print("Set Amount to Deposit")
                    self.amount = self.am.check_balance()
                    new_balance = account['Balance'] + self.amount
                    sql = "UPDATE account SET Balance=%s WHERE accno=%s"
                    self.ps = self.con.cursor()
                    self.ps.execute(sql, (new_balance, acc))
                    if self.ps.rowcount > 0:
                        formatted_date = datetime.now().strftime("%Y-%m-%d")
                        transaction_id = self.generate_transaction_id()
                        sql = "INSERT INTO transaction (transaction_ID, from_accNo, to_accNo, amount, Date) VALUES (%s, %s, %s, %s, %s)"
                        self.ps.execute(sql, (transaction_id, acc, acc, self.amount, formatted_date))
                        if self.ps.rowcount > 0:
                            self.con.commit() 
                            print(f"Rs:- {self.amount}/- Is Deposited Successfully")
                            print("Transaction recorded successfully")
                        else:
                            self.con.rollback()
                            print("Failed to record transaction")
                    else:
                        self.con.rollback() 
                        print("Payment failed")
            except mysql.connector.Error as e:
                self.con.rollback() 
                print(f"An error occurred: {e}")

    def account_to_account(self):
        from_acc = self.login()
        if from_acc:
            to_acc = input("Enter Receiver Account Number: ")
            if self.am.check_account(to_acc):
                if to_acc != from_acc:
                    self.cursor.execute("SELECT Balance FROM account WHERE accno = %s", (to_acc,))
                    to_account = self.cursor.fetchone()
                    if to_account:
                        print("Set Amount to Transfer")
                        self.amount = self.am.check_balance()
                        self.cursor.execute("SELECT Balance FROM account WHERE accno = %s", (from_acc,))
                        from_account = self.cursor.fetchone()
                        if from_account['Balance'] >= self.amount:
                            new_from_balance = from_account['Balance'] - self.amount
                            sql = "UPDATE account SET Balance=%s WHERE accno=%s"
                            self.ps = self.con.cursor()
                            self.ps.execute(sql, (new_from_balance, from_acc))
                            if self.ps.rowcount > 0:
                                new_to_balance = to_account['Balance'] + self.amount
                                sql = "UPDATE account SET Balance=%s WHERE accno=%s"
                                self.ps.execute(sql, (new_to_balance, to_acc))
                                if self.ps.rowcount > 0:
                                    formatted_date = datetime.now().strftime("%Y-%m-%d")
                                    transaction_id = self.generate_transaction_id()
                                    sql = "INSERT INTO transaction (transaction_ID, from_accNo, to_accNo, amount, Date) VALUES (%s, %s, %s, %s, %s)"
                                    self.ps.execute(sql, (transaction_id, from_acc, to_acc, self.amount, formatted_date))
                                    if self.ps.rowcount > 0:
                                        self.con.commit() 
                                        print(f"{self.amount} Rs/- Transferred From {from_acc} TO {to_acc} Successfully")
                                        self.loan.set_data(from_acc)
                                    else:
                                        self.con.rollback() 
                                        print("Failed to record transaction")
                                else:
                                    self.con.rollback() 
                                    print("Payment failed")
                        else:
                            print("Insufficient Balance to Transfer")
                    else:
                        print("Receiver Account Number Not Found")
                else:
                    print("Receiver and Sender Account Cannot Be The Same")
            else:
                print("Invalid Receiver Account Number")

    @staticmethod
    def make_passbook(acc_no, balance, date, mode, amount):
        with open(f"PassBook_For_{acc_no}.txt", "a") as f:
            f.write(f"{amount}_{mode}_BY_Self_ON_{date}_Balance: {balance}\n")

    @staticmethod
    def make_passbook_account_to_account(from_acc_no, from_balance, to_balance, date, mode1, mode2, amount, to_acc_no):
        with open(f"PassBook_For_{from_acc_no}.txt", "a") as fw1:
            with open(f"PassBook_For_{to_acc_no}.txt", "a") as fw2:
                fw1.write(f"{amount}_{mode1}_TO_{to_acc_no}_ON_{date}_Balance: {from_balance}\n")
                fw2.write(f"{amount}_{mode2}_FROM_{from_acc_no}_ON_{date}_Balance: {to_balance}\n")

    def check_for_withdraw(self, acc_no):
        sql = "SELECT Balance FROM account WHERE accno=%s"
        self.ps = self.con.cursor()
        self.ps.execute(sql, (acc_no,))
        result = self.ps.fetchone()
        if result:
            return result['Balance']
        return 0

    @staticmethod
    def generate_transaction_id():
        return ''.join([str(random.randint(0, 9)) for _ in range(10)])

    def print_passbook(self):
        try:
            acc = input("Enter Account Number: ")
            if self.am.check_account(acc):
                self.cursor.execute("SELECT PIN FROM account WHERE accno = %s", (acc,))
                account = self.cursor.fetchone()
                if account:
                    self.pin = self.am.check_pin()
                    if account['PIN'] == self.pin:
                        filename = f"PassBook_For_{acc}.txt"
                        with open(filename, "w") as f:
                            f.write(f"Passbook for Account Number: {acc}\n")
                            f.write("---------------------------------------------------\n")
                            f.write("Date       | Transaction ID | From Account | To Account | Amount\n")
                            f.write("---------------------------------------------------\n")
                            
                            self.cursor.execute("SELECT * FROM transaction WHERE from_accNo = %s", (acc,))
                            outgoing_transactions = self.cursor.fetchall()
                            for transaction in outgoing_transactions:
                                f.write(f"{transaction['Date']} | {transaction['transaction_ID']} | {transaction['from_accNo']} | {transaction['to_accNo']} | {transaction['amount']}\n")
                            
                            self.cursor.execute("SELECT * FROM transaction WHERE to_accNo = %s AND from_accNo != %s", (acc, acc))
                            incoming_transactions = self.cursor.fetchall()
                            for transaction in incoming_transactions:
                                f.write(f"{transaction['Date']} | {transaction['transaction_ID']} | {transaction['from_accNo']} | {transaction['to_accNo']} | +{transaction['amount']}\n")
                            
                            f.write("---------------------------------------------------\n")
                        print(f"Passbook has been saved to {filename}")
                    else:
                        print("Invalid PIN")
                else:
                    print("Account Number Not Found")
            else:
                print("Invalid Account Number")
        except Exception as e:
            print(f"An error occurred: {e}")

