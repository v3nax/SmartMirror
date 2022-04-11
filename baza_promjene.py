
import sqlite3

select_query = "SELECT sqlite_version();"

try:

    sqliteConnection = sqlite3.connect('vrijeme.db')

    cursor = sqliteConnection.cursor()
    print("Baza je USPJESNO kreirana te je aplikacija spojena na SQLite")

    cursor.execute(select_query)

    records = cursor.fetchall()

    print("SQLite verzija je: ", records)
 
    cursor.close()
    print("Resursi SQLite CURSOR objekta su uspješno otpušteni")

except sqlite3.Error as error:
    print("ERROR - Dogodila se greska prilikom pokusaja spajanja na SQLite:", error)

finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("SQLite konekcija je uspješno zatvorena")



create_table_query = '''CREATE TABLE IF NOT EXISTS Promjene (
                                id INT PRIMARY KEY NULL,
                                datum TEXT NOT NULL,
                                vrijeme TEXT NOT NULL,
                                temperatura INT NOT NULL,
                                vlaznost INT NOT NULL,
                                tlak REAL NOT NULL);'''
database_name = 'vrijeme.db'


try:
    sqliteConnection = sqlite3.connect(database_name)
    cursor = sqliteConnection.cursor()
    print(f"SQLite baza {database_name} je USPJESNO kreirana te je aplikacija spojena na bazu")
    
    cursor.execute(create_table_query)
    
    sqliteConnection.commit()

    print("Nova tabela Event je uspjesno kreirana")
    
    cursor.close()
    print("Resursi SQLite CURSOR objekta su uspješno otpušteni")
except sqlite3.Error as error:
    print("ERROR - Dogodila se greska prilikom pokusaja spajanja na SQLite:", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("SQLite konekcija je uspješno zatvorena")


def sql_removeduplicates():
    con = sqlite3.connect('vrijeme.db')
    with con:    
        cur = con.cursor()    
        cur.execute("SELECT temperatura, vlaznost, tlak, COUNT (*) FROM Promjene GROUP BY temperatura, vlaznost, tlak HAVING COUNT (*) > 1")
        rows = cur.fetchall()
        con.commit()
        for row in rows:
            #cur.execute('DELETE FROM Promjene')
        
            print(row)

sql_removeduplicates()
