import sqlite3
import csv

def init_db():
    connection = sqlite3.connect('legislation.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    # Read data from CSV and insert into database
    with open('State AI tracker.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cur.execute("""
                INSERT INTO state_legislation
                (state, bill_number, scope, key_provisions, summary, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (row['State'], row['Bill Number'], row['Scope'],
                  row['Key Provisions'], row['Summary'], row['Status']))

    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized with data from CSV.")
