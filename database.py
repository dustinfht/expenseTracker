import sqlite3
import os
from expense import Expense


class DatabaseConnector:
    table_name = "expenses"

    def __init__(self, database_name):
        self.database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), database_name)
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()

    def setup_tables(self):
        sql = f"CREATE TABLE IF NOT EXISTS {self.table_name}(" \
              "id INTEGER PRIMARY KEY, " \
              "type TEXT, " \
              "amount REAL, " \
              "cause TEXT, " \
              "timestamp TEXT);"

        self.cursor.execute(sql)

    def add_expense(self, amount, cause, timestamp):
        if not is_int(amount):
            return False

        amount = int(amount)
        sql = f"INSERT INTO {self.table_name} " \
              f"(type, amount, cause, timestamp)" \
              f"VALUES ('EXPENSE', {amount}, '{cause}', '{timestamp}');"

        self.cursor.execute(sql)
        self.connection.commit()
        print("Added expense to database.")

    def get_expenses(self):
        sql = f"SELECT * FROM {self.table_name};"
        self.cursor.execute(sql)

        entries = []
        for entry in self.cursor:
            entries.append(Expense(entry[0], entry[2], entry[3], entry[4]))

        print(f"Found {len(entries)} entries in database.")
        return entries

    def delete_expense(self, expense_id):
        sql = f"DELETE FROM {self.table_name} WHERE id = {expense_id}"
        self.cursor.execute(sql)
        self.connection.commit()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
