from gui import Gui
from database import DatabaseConnector

database_connector = DatabaseConnector("database.db")


def main():
    database_connector.connect()
    database_connector.setup_tables()
    print("Connected to database.")

    gui = Gui(database_connector)
    gui.show_main()

    database_connector.disconnect()
    print("Disconnected from database.")


if __name__ == '__main__':
    main()
