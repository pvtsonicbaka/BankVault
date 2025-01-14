import mysql.connector
from CustomerManagement import CustomerManagement
from AccountManagement import AccountManagement
from TransactionManager import TransactionManager
from DataStructureImplementation import DataStructureImplementation
from Loan import Loan


class BankManagementCLI:

    def __init__(self):
        print("Initializing Bank Management System...")
        self.cm = CustomerManagement()
        self.am = AccountManagement(self.cm)  
        self.tm = TransactionManager(self.cm)
        self.dsi = DataStructureImplementation()
        self.loan = Loan()
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
            print("12 : Transaction History")
            print("13 : Check Credit Score and Loan Status")
            print("14 : Generate List of Top Loan Approvals")
            print("15 : Exit")
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
                    acc_no = input("Enter Account Number: ").strip()
                    if self.am.check_account(acc_no):
                        self.dsi.display_transaction_history(acc_no)
                    else:
                        print("Invalid Account Number")
                elif choice == "13":
                    self.loan.get_status()
                elif choice == "14":
                    self.dsi.generate_loan_list()
                elif choice == "15":
                    print("Thank you for using the Bank Management System. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please select a valid option.")
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please try again.")

if __name__ == "__main__":
    BankManagementCLI().main()
