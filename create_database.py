import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"C:\sqlite\Lab2.db"

    sql_create_immediate_table = """ CREATE TABLE IF NOT EXISTS request_immediate (
                                        id integer PRIMARY KEY ASC,
                                        name varchar(250) NOT NULL,
                                        location varchar(250) NOT NULL,
                                        destination varchar(250) NOT NULL,
                                        passengers integer NOT NULL,
                                        date_created varchar(250) NOT NULL); """

    sql_create_scheduled_table = """ CREATE TABLE IF NOT EXISTS request_scheduled (
                                        id integer PRIMARY KEY,
                                        name varchar(250) NOT NULL,
                                        location varchar(250) NOT NULL,
                                        destination varchar(250) NOT NULL,
                                        passengers integer NOT NULL, 
                                        datetime varchar(250) NOT NULL,
                                        date_created varchar(250) NOT NULL); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_immediate_table)
        create_table(conn, sql_create_scheduled_table)
    else:
        print("Cannot create database connection.")


if __name__ == '__main__':
    main()
