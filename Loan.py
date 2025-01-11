import mysql.connector

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
            connection = mysql.connector.connect(
                host="localhost",
                user="your_user",
                password="your_password",
                database="your_database"
            )
            return connection
        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")
            exit()

    def set_data(self, accno):
        try:
            cursor = self.con.cursor()

            # Calling stored procedure for setting data
            cursor.callproc('setData', [accno])
            self.id = cursor.fetchall()[0][1]
            self.name = cursor.fetchall()[0][2]

            # Fetch count of transactions
            cursor.callproc('getCount', [self.id])
            self.count = cursor.fetchall()[0][1]

            # Fetch balance
            cursor.callproc('getBalance', [self.id])
            self.update_balance = cursor.fetchall()[0][1]

            if self.count <= 1:
                self.credit = 0
                self.status = "Not Eligible"
                self.insert_data()
            else:
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

                if self.credit >= 3:
                    self.status = "Eligible"
                else:
                    self.status = "Not Eligible"
                self.update_data()

        except mysql.connector.Error as e:
            print(f"Error in setting data: {e}")

    def insert_data(self):
        try:
            cursor = self.con.cursor()
            sql = "INSERT INTO loan (cid, name, credit_score, status) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (self.id, self.name, self.credit, self.status))
            self.con.commit()
            print("Success")
        except mysql.connector.Error as e:
            print(f"Error in inserting data: {e}")

    def update_data(self):
        try:
            cursor = self.con.cursor()
            sql = "UPDATE loan SET credit_score = %s, status = %s WHERE cid = %s"
            cursor.execute(sql, (self.credit, self.status, self.id))
            self.con.commit()
        except mysql.connector.Error as e:
            print(f"Error in updating data: {e}")

    def get_status(self):
        try:
            checkid = int(input("Enter Customer ID: "))
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
