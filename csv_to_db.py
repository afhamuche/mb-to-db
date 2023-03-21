import sqlite3
import csv

csvFileName = input("Enter csv filename: ")
createTable = input("Create new table? y/n: ")

# Connect to the database
conn = sqlite3.connect('trades.db')
c = conn.cursor()

if createTable[0] == 'y':

    print('Create table \'trades\'')

    # Create a table to store the data
    c.execute('''CREATE TABLE trades
                (amount REAL, date DOUBLE, price REAL, tid DOUBLE, type TEXT, satoshi DOUBLE, volume REAL)''')

# Open the CSV file and insert the data into the database
with open(csvFileName, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) # Skip the header row
    for row in reader:
        c.execute("INSERT INTO trades (amount, date, price, tid, type, satoshi, volume) VALUES (?, ?, ?, ?, ?, ?, ?)", row)

# Commit the changes and close the connection
conn.commit()
conn.close()
