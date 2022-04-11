
import sqlite3

select_query = "SELECT sqlite_version();"

try:

    sqliteConnection = sqlite3.connect('event.db')

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



create_table_query = '''CREATE TABLE IF NOT EXISTS Planer (
                                id INT PRIMARY KEY NULL,
                                datum TEXT NOT NULL,
                                vrijeme TEXT NOT NULL,
                                dan TEXT NOT NULL,
                                naslov TEXT NOT NULL,
                                dogadaj TEXT NOT NULL);'''
database_name = 'event.db'


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



