import random
import os
from datetime import datetime
import mysql.connector
import AccountManagement
import Loan
class TransactionManager:
    def __init__(self):
        self.am = AccountManagement()  # Assuming this is defined elsewhere
        self.loan = Loan()  # Assuming this is defined elsewhere
        self.sc = input
        self.pin = None
        self.to_cid = None
        self.from_cid = None
        self.DateOfTransaction = None
        self.balance = None
        self.amount = None
        self.acc_no = None
        self.con = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="your_password", 
            database="your_database"
        )
        self.ps = None

    def with_draw(self):
        self.am.getAccID()
        acc = input("Enter Account Number: ")
        if self.am.checkAccount(acc):
            if acc in self.am.hsacc:
                self.pin = self.am.checkPIN()
                if self.am.hsacc[acc] == self.pin:
                    print("Set Amount to Withdraw")
                    self.amount = self.am.checkBalance()
                    balance = self.check_for_withdraw(acc)
                    if balance >= self.amount:
                        new_balance = balance - self.amount
                        sql = "UPDATE account SET Balance=%s WHERE accno=%s"
                        self.ps = self.con.cursor()
                        self.ps.execute(sql, (new_balance, acc))
                        if self.ps.rowcount > 0:
                            print(f"Rs:- {self.amount}/- Is Withdrawn Successfully")
                            formatted_date = datetime.now().strftime("%Y-%m-%d")
                            self.make_passbook(acc, new_balance, formatted_date, "Withdraw", self.amount)
                        else:
                            print("Payment failed")
                    else:
                        print("Insufficient Balance to Withdraw")
                else:
                    print("Invalid PIN")
            else:
                print("Account Number Not Found")
        else:
            print("Invalid Account Number")

    def deposit(self):
        self.am.getAccID()
        acc = input("Enter Account Number: ")
        if self.am.checkAccount(acc):
            if acc in self.am.hsacc:
                self.pin = self.am.checkPIN()
                if self.am.hsacc[acc] == self.pin:
                    print("Set Amount to Deposit")
                    self.amount = self.am.checkBalance()
                    balance = self.check_for_withdraw(acc)
                    new_balance = balance + self.amount
                    sql = "UPDATE account SET Balance=%s WHERE accno=%s"
                    self.ps = self.con.cursor()
                    self.ps.execute(sql, (new_balance, acc))
                    if self.ps.rowcount > 0:
                        print(f"Rs:- {self.amount}/- Is Deposited Successfully")
                        formatted_date = datetime.now().strftime("%Y-%m-%d")
                        self.make_passbook(acc, new_balance, formatted_date, "Deposit", self.amount)
                    else:
                        print("Payment failed")
                else:
                    print("Invalid PIN")
            else:
                print("Account Number Not Found")
        else:
            print("Invalid Account Number")

    def account_to_account(self):
        self.am.getAccID()
        from_acc = input("Enter Sender Account Number: ")
        if self.am.checkAccount(from_acc):
            if from_acc in self.am.hsacc:
                self.pin = self.am.checkPIN()
                if self.am.hsacc[from_acc] == self.pin:
                    to_acc = input("Enter Receiver Account Number: ")
                    if self.am.checkAccount(to_acc):
                        if to_acc != from_acc:
                            if to_acc in self.am.hsacc:
                                print("Set Amount to Transfer")
                                self.amount = self.am.checkBalance()
                                from_balance = self.check_for_withdraw(from_acc)
                                to_balance = self.check_for_withdraw(to_acc)
                                if from_balance >= self.amount:
                                    new_from_balance = from_balance - self.amount
                                    sql = "UPDATE account SET Balance=%s WHERE accno=%s"
                                    self.ps = self.con.cursor()
                                    self.ps.execute(sql, (new_from_balance, from_acc))
                                    if self.ps.rowcount > 0:
                                        new_to_balance = to_balance + self.amount
                                        sql = "UPDATE account SET Balance=%s WHERE accno=%s"
                                        self.ps.execute(sql, (new_to_balance, to_acc))
                                        if self.ps.rowcount > 0:
                                            formatted_date = datetime.now().strftime("%Y-%m-%d")
                                            self.make_passbook_account_to_account(from_acc, new_from_balance, new_to_balance, formatted_date, "Transfer", "Received", self.amount, to_acc)
                                            transaction_id = self.generate_transaction_id()
                                            sql = "INSERT INTO transaction VALUES(%s, %s, %s, %s, %s)"
                                            self.ps.execute(sql, (transaction_id, from_acc, to_acc, self.amount, formatted_date))
                                            if self.ps.rowcount > 0:
                                                print(f"{self.amount} Rs/- Transferred From {from_acc} TO {to_acc} Successfully")
                                                self.loan.set_data(from_acc)
                                        else:
                                            print("Payment failed")
                                    else:
                                        print("Payment failed")
                                else:
                                    print("Insufficient Balance to Transfer")
                            else:
                                print("Receiver Account Number Not Found")
                        else:
                            print("Receiver and Sender Account Cannot Be The Same")
                    else:
                        print("Invalid Receiver Account Number")
                else:
                    print("Invalid PIN")
            else:
                print("Account Number Not Found")
        else:
            print("Invalid Account Number")

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
        sql = "SELECT * FROM account WHERE accno=%s"
        self.ps = self.con.cursor()
        self.ps.execute(sql, (acc_no,))
        result = self.ps.fetchone()
        if result:
            return result[1]  # Assuming balance is at index 1
        return 0

    @staticmethod
    def generate_transaction_id():
        return ''.join([str(random.randint(0, 9)) for _ in range(10)])

    def print_passbook(self):
        try:
            self.am.getAccID()
            acc = input("Enter Account Number: ")
            if self.am.checkAccount(acc):
                if acc in self.am.hsacc:
                    self.pin = self.am.checkPIN()
                    if self.am.hsacc[acc] == self.pin:
                        with open(f"PassBook_For_{acc}.txt", "r") as fr:
                            print(fr.read())
                    else:
                        print("Invalid PIN")
                else:
                    print("Account Number Not Found")
            else:
                print("Invalid Account Number")
        except Exception as e:
            print("Transaction has not been done yet")

