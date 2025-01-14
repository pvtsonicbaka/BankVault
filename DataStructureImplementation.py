import mysql.connector
from collections import deque
import logging
from Connector import Connector
# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Loan:
    def __init__(self, loan_id, name, credit, status):
        self.id = loan_id
        self.name = name
        self.credit = credit
        self.status = status


class DataStructureImplementation:
    def __init__(self):
        self.head = None
        self.stack = deque()
        self.db_connection = self.connect_to_db()

    class Node:
        def __init__(self, loan):
            self.loan = loan
            self.next = None

    def connect_to_db(self):
        try:
            connection = Connector().get_connection()
            
            
            logging.info("Connected to database successfully.")
            return connection
        except mysql.connector.Error as e:
            logging.error(f"Database connection error: {e}")
            exit()

    # Stack Operations
    def push(self, data):
        self.stack.append(data)

    def pop(self):
        if not self.stack:
            return "No Record Found"
        return self.stack.pop()

    def display(self):
        print("---------------------------------------------------")
        for record in reversed(self.stack):
            print(record)
            print()
        print("---------------------------------------------------")

    # Linked List for Loans
    def insert(self, loan):
        new_node = self.Node(loan)
        if not self.head or self.head.loan.credit < new_node.loan.credit:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and current.next.loan.credit >= new_node.loan.credit:
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def set_list(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM Loan WHERE status='Eligible'")
            for row in cursor.fetchall():
                loan = Loan(row[0], row[1], row[2], row[3])
                self.insert(loan)
            logging.info("Loan list set successfully.")
        except mysql.connector.Error as e:
            logging.error(f"Error fetching loans: {e}")

    def generate_list(self):
        try:
            with open("Top_Customer_for_Loan_Approval.txt", "w") as file:
                current = self.head
                if not current:
                    print("No customers eligible for loan")
                    return
                while current:
                    file.write(f"Customer ID: {current.loan.id}\n")
                    file.write(f"Customer Name: {current.loan.name}\n")
                    file.write(f"Credit Score: {current.loan.credit}\tStatus: {current.loan.status}\n")
                    file.write("--------------------------------------------------------------\n\n")
                    current = current.next
            logging.info("Loan list successfully generated.")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

    # Passbook Operations
    def load_passbook(self, acc):
        try:
            with open(f"PassBook_For_{acc}.txt", "r") as file:
                for line in file:
                    parts = line.strip().split("_")
                    if len(parts) >= 6:
                        amount = parts[0]
                        method = parts[1]
                        sign = "+" if method in ("Received", "Deposit") else "-"
                        account_no = parts[3]
                        date = parts[5]
                        self.push(f"Date: {date}\nAccount Number: {account_no}\t{sign}{amount}")

                self.passbook_menu()
        except FileNotFoundError:
            print("No Transaction Done Yet")
        except Exception as e:
            logging.error(f"Error loading passbook: {e}")

    def passbook_menu(self):
        while True:
            print("1 - View Transaction History")
            print("2 - Retrieve and Delete Latest Transaction")
            print("3 - Exit")
            choice = input("Enter Your Choice: ")

            if choice == "1":
                self.display()
            elif choice == "2":
                print("---------------------------------------------------")
                print(self.pop())
                print("---------------------------------------------------")
            elif choice == "3":
                break
            else:
                print("Invalid Input")


# Example Usage
if __name__ == "__main__":
    dsi = DataStructureImplementation()
    # Load loan data into linked list
    dsi.set_list()
    # Generate loan approval list
    dsi.generate_list()
    # Load passbook for account number 12345
    dsi.load_passbook(12345)
