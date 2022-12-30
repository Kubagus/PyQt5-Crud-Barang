import sqlite3 as sql

# def main():
try:
    db = sql.connect('dbToko.db')
    print("Database exist")
except:
    print("failed to connect database")
finally:
    db.close()

# if __name__ == "__main__":
#     main()