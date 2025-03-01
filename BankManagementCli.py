import mysql.connector
from CustomerManagement import CustomerManagement
from AccountManagement import AccountManagement
from TransactionManager import TransactionManager
from Admin import Admin
from Connector import Connector



class BankManagementCLI:
    def __init__(self):
        print("Initializing Bank Management System...")
        self.connector = Connector()
        self.connection = self.connector.get_connection()
        self.cm = CustomerManagement(self.connection)
        self.am = AccountManagement(self.cm, self.connection)
        self.tm = TransactionManager(self.cm, self.connection)
        self.admin = Admin(self.connection)
        print("Initialization Complete. Welcome to the Bank Management System!")

    def main(self):
        while True:
            print("\n--------------------------------------------")
            print("Bank Management System Menu:")
            print("1 : Register a Customer")
            print("2 : Update Customer Information")
            print("3 : Delete Customer")
            print("4 : Add Account")
            print("5 : Delete Account")
            print("6 : Update PIN")
            print("7 : Withdraw")
            print("8 : Deposit")
            print("9 : Account to Account Transfer")
            print("10 : See Balance")
            print("11 : Retrieve Passbook")
            print("12 : Exit")
            print("--------------------------------------------")
            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    self.cm.add_customer()
                elif choice == "2":
                    self.cm.update_customer()
                elif choice == "3":
                    self.cm.delete_customer()
                elif choice == "4":
                    self.am.add_account()
                elif choice == "5":
                    self.am.del_account()
                elif choice == "6":
                    self.am.update_account_pin()
                elif choice == "7":
                    self.tm.with_draw()
                elif choice == "8":
                    self.tm.deposit()
                elif choice == "9":
                    self.tm.account_to_account()
                elif choice == "10":
                    self.am.view_balance()
                elif choice == "11":
                    self.tm.print_passbook()
                elif choice == "12":
                    print("Thank you for using the Bank Management System. Goodbye!")
                    break
                elif choice == "99":
                    self.admin_menu()
                else:
                    print("Invalid choice. Please select a valid option.")
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please try again.")

    def admin_menu(self):
        admin_id=input("enter admin_id :")
        password=input("enter password :")
        while True and self.admin.verify_credentials(admin_id,password):
            print("\n--------------------------------------------")
            print("Admin Functions Menu:")
            print("1 : View All Customers")
            print("2 : View All Accounts")
            print("3 : View All Transactions")
            print("4 : Back to Main Menu")
            print("--------------------------------------------")
            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    self.admin.view_all_customers()
                elif choice == "2":
                    self.admin.view_all_accounts()
                elif choice == "3":
                    self.admin.view_all_transactions()
                elif choice == "4":
                    break
                else:
                    print("Invalid choice. Please select a valid option.")
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please try again.")
        else:
            print()
            print("::::::::::::::::::::::invalid credentials:::::::::::::::::::::::::")
if __name__ == "__main__":
    BankManagementCLI().main()

