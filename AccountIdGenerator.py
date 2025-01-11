import random

class AccountIdGenerator:

    @staticmethod
    def generate_numeric_account_id():
        account_id = ''.join(str(random.randint(0, 9)) for _ in range(12))
        return account_id


if __name__ == "__main__":
    account_id = AccountIdGenerator.generate_numeric_account_id()
    print(account_id)
