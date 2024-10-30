import sqlite3


def create_database() -> None:
    # Your solution goes here.
    # create a database named mydatabase.db
    connection = sqlite3.connect('mydatabase.db')
    # create a cursor object for the database
    cursor = connection.cursor()

    # create a table named company
    cursor.execute('CREATE TABLE company (id INTEGER PRIMARY KEY, \
        name TEXT)')

    # insert 1000 rows of data into the company table
    for i in range(1000):
        # give a list of characters to be selected from
        char = 'abcdefghijklmnopqrstuvwxyz'
        # create a name for the company with 5 characters
        company_name = ''
        for j in [1,5,10,20,50]:
            company_name += char[(i + j) % 26]
        # insert the company to the table
        cursor.execute('INSERT INTO company VALUES ({}, "{}")'.format(i, company_name))

    # commit the changes to the database
    connection.commit()
