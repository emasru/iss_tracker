from databasemanager import Database
from os import system

d = Database("recorded_positions")
while True:
    run_id = input("Enter the run ID for the database: ")
    system("cls")
    try:
        run_id = int(run_id)
    except ValueError:
        run_id = None

    for row in d.read_from_database(run_id):
        print(row)