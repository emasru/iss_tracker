from databasemanager import Database
from os import system
from plottingcontroller import plot

d = Database("recorded_positions")
while True:
    print("the number of runids are: %d, if you want to read all input None" % (d.largest_identifier()+1))
    run_id = input("Enter the run ID for the database: ")
    system("cls")
    try:
        run_id = int(run_id)
    except ValueError:
        run_id = None

    for row in d.read_from_database(run_id):
        print(row)
    
    plot1 = plot(d.read_from_database(run_id))