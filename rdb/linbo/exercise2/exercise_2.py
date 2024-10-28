import sqlite3


def create_database() -> None:
    # Your solution goes here.
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS mytable 
        (id INT PRIMARY KEY NOT NULL,
        value TEXT NOT NULL)
    ''')
    
    data = [(i,f"Value{i}") for i in range(1,1001)]
    
    cursor.executemany("INSERT INTO mytable VALUES (?,?)",data)
    
    conn.commit()
    conn.close()
