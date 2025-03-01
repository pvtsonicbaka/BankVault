import re
import mysql.connector
from mysql.connector import Error

class CustomerManagement:
    def __init__(self, connection):
        try:
            self.con = connection
            self.cursor = self.con.cursor(dictionary=True)
            self.hscid = set()
        except AttributeError:
            print("Error: Connector class is not implemented correctly.")
        except Error as e:
            print(f"Database Connection Error: {e}")

    def add_customer(self):
        try:
            name = input("Enter Name of Customer: ")
            if self.check_name(name):
                password = input("Enter Password: ")
                address = input("Enter Address: ")
                phone = self.check_number()
                gender = self.select_gender()
                aadhar = self.check_aadhar()
                age = self.check_age()

                sql = """INSERT INTO customer (cname, cpass, cadd, cphone, gender, aadhar, age) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                values = (name, password, address, phone, gender, aadhar, age)
                self.cursor.execute(sql, values)
                self.con.commit()

                if self.cursor.rowcount > 0:
                    print("Customer Added Successfully")
                    self.cursor.execute("SELECT cid FROM customer WHERE aadhar = %s", (aadhar,))
                    result = self.cursor.fetchone()
                    if result:
                        cid = result["cid"]
                        self.cursor.callproc('insertData', [cid, name])
                else:
                    print("Customer Not Added")
            else:
                print("Invalid Name")
        except Error as e:
            print(f"Error: {e}")

    def delete_customer(self):
        try:
            name = input("Enter Name of Customer: ")
            if self.check_name(name):
                password = input("Enter Password: ")
                cid = input("Enter ID Number: ")

                if not cid.isdigit():
                    print("Invalid ID. It should be numeric.")
                    return

                sql = """DELETE FROM customer WHERE cname = %s AND cpass = %s AND cid = %s"""
                self.cursor.execute(sql, (name, password, int(cid)))
                self.con.commit()

                if self.cursor.rowcount > 0:
                    self.cursor.execute("DELETE FROM account WHERE cid = %s", (cid,))
                    self.con.commit()
                    print("Customer Deleted Successfully")
                else:
                    print("Customer Not Found")
            else:
                print("Invalid Name")
        except Error as e:
            print(f"Error: {e}")

    def update_customer(self):
        try:
            self.get_ids()
            cid = input("Enter ID Number: ")

            if not cid.isdigit():
                print("Invalid ID. It should be numeric.")
                return

            cid = int(cid)
            if cid in self.hscid:
                name = input("Enter Name: ")
                if self.check_name(name):
                    password = input("Enter Password: ")
                    address = input("Enter Address: ")
                    phone = self.check_number()
                    gender = self.select_gender()
                    aadhar = self.check_aadhar()
                    age = self.check_age()

                    sql = """UPDATE customer SET cname = %s, cpass = %s, cadd = %s, cphone = %s, 
                             gender = %s, aadhar = %s, age = %s WHERE cid = %s"""
                    values = (name, password, address, phone, gender, aadhar, age, cid)
                    self.cursor.execute(sql, values)
                    self.con.commit()

                    if self.cursor.rowcount > 0:
                        print("Customer Details Updated Successfully")
                else:
                    print("Invalid Name")
            else:
                print("ID Not Found")
        except Error as e:
            print(f"Error: {e}")

    def check_name(self, name):
        return bool(re.fullmatch(r"[A-Za-z ]+", name))

    def check_number(self):
        while True:
            number = input("Enter Mobile Number: ")
            if len(number) == 10 and number.isdigit():
                return number
            print("Invalid Mobile Number. It should contain 10 digits.")

    def check_aadhar(self):
        while True:
            aadhar = input("Enter Aadhaar Card Number: ")
            if len(aadhar) == 12 and aadhar.isdigit():
                return aadhar
            print("Invalid Aadhaar Card Number. It should contain 12 digits.")

    def check_age(self):
        while True:
            age = input("Enter Age: ")
            if age.isdigit() and 18 <= int(age) <= 100:
                return int(age)
            print("Invalid Age. It should be a numeric value between 18 and 100.")

    def select_gender(self):
        while True:
            print("1-Male \t 2-Female \t 3-Other")
            choice = input("Enter your choice: ")
            if choice == "1":
                return "Male"
            elif choice == "2":
                return "Female"
            elif choice == "3":
                return "Other"
            print("Invalid choice. Please select a valid option.")

    def get_ids(self):
        try:
            self.hscid.clear()
            self.cursor.execute("SELECT cid FROM customer")
            for row in self.cursor.fetchall():
                self.hscid.add(row["cid"])
        except Error as e:
            print(f"Error fetching IDs: {e}")
