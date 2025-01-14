import mysql.connector
from Connector import Connector


class Loan:
    def __init__(self):
        self.con = self.connect_to_db()
        self.id = None
        self.count = None
        self.name = None
        self.credit = None
        self.update_balance = None
        self.status = None

    def connect_to_db(self):
        try:
            connector = Connector()
            return connector.get_connection()
        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")
            exit()

    def set_data(self, accno):
        try:
            cursor = self.con.cursor()

            # Calling stored procedure for setting data
            cursor.callproc('setData', [accno])
            result = cursor.fetchall()
            self.id = result[0][1]
            self.name = result[0][2]

            # Fetch count of transactions
            cursor.callproc('getCount', [self.id])
            self.count = cursor.fetchall()[0][1]

            # Fetch balance
            cursor.callproc('getBalance', [self.id])
            self.update_balance = cursor.fetchall()[0][1]

            # Evaluate credit and status
            if self.count <= 1:
                self.credit = 0
                self.status = "Not Eligible"
                self.insert_data()
            else:
                self.evaluate_credit_and_status()
                self.update_data()

        except mysql.connector.Error as e:
            print(f"Error in setting data: {e}")

    def evaluate_credit_and_status(self):
        if self.count >= 10:
            self.credit = 5
        elif self.count >= 5:
            if self.update_balance >= 5000:
                self.credit = 4
            else:
                self.credit = 3
        else:
            if self.update_balance >= 5000:
                self.credit = 2
            else:
                self.credit = 1

        self.status = "Eligible" if self.credit >= 3 else "Not Eligible"

    def insert_data(self):
        try:
            cursor = self.con.cursor()
            sql = "INSERT INTO loan (cid, name, credit_score, status) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (self.id, self.name, self.credit, self.status))
            self.con.commit()
            print("Data inserted successfully")
        except mysql.connector.Error as e:
            print(f"Error in inserting data: {e}")

    def update_data(self):
        try:
            cursor = self.con.cursor()
            sql = "UPDATE loan SET credit_score = %s, status = %s WHERE cid = %s"
            cursor.execute(sql, (self.credit, self.status, self.id))
            self.con.commit()
            print("Data updated successfully")
        except mysql.connector.Error as e:
            print(f"Error in updating data: {e}")

    def get_status(self):
        try:
            checkid = input("Enter Customer ID: ")
            if not checkid.isdigit():
                print("Invalid Customer ID")
                return
            checkid = int(checkid)

            cursor = self.con.cursor()
            sql = "SELECT * FROM loan WHERE cid = %s"
            cursor.execute(sql, (checkid,))
            result = cursor.fetchone()

            if result:
                print(f"Credit Score: {result[2]}")
                print(f"Status: {result[3]}")
            else:
                print("Record Not Found")
        except mysql.connector.Error as e:
            print(f"Error in retrieving status: {e}")
