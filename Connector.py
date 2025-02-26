import mysql.connector
from mysql.connector import Error


class Connector:
    def __init__(self):
        self.host = "localhost"
        self.database = "bank"
        self.user = "root"
        self.password = ""  
        self.con = None

    def connect(self):
        try:
            self.con = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            if self.con.is_connected():
                print("✅ Connected to Database Successfully")
            else:
                print("❌ Connection to database failed!")
        except Error as e:
            print(f"⚠️ Error while connecting to MySQL: {e}")

    def get_connection(self):
        if self.con is None or not self.con.is_connected():
            print("🔄 Reconnecting to the database...")
            self.connect()
        return self.con


if __name__ == "__main__":
    connector = Connector()
    connection = connector.get_connection()
    if connection:
        print("✅ Connection object ready to use.")
    else:
        print("❌ Could not establish a connection.")
