import mysql.connector
import yaml

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    host = app_config['datastore']['hostname']
    user = app_config['datastore']['user']
    password = app_config['datastore']['password']
    database = app_config['datastore']['db']

db_create = mysql.connector.connect(host=host, user=user, password=password)
mycursor = db_create.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS events")

db_conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
db_cursor = db_conn.cursor()

db_cursor.execute('''
                  CREATE TABLE request_immediate
                  (id INT NOT NULL AUTO_INCREMENT,
                   name VARCHAR(250) NOT NULL,
                   location VARCHAR(250) NOT NULL,
                   destination VARCHAR(250) NOT NULL,
                   passengers INT NOT NULL,
                   date_created VARCHAR(100) NOT NULL,
                   CONSTRAINT immediate_reqest_pk PRIMARY KEY (id))''')

db_cursor.execute('''
                  CREATE TABLE request_scheduled
                  (id INT NOT NULL AUTO_INCREMENT,
                   name VARCHAR(250) NOT NULL,
                   location VARCHAR(250) NOT NULL,
                   destination VARCHAR(250) NOT NULL,
                   passengers INT NOT NULL,
                   datetime VARCHAR(100) NOT NULL,
                   date_created VARCHAR(100) NOT NULL,
                   CONSTRAINT scheduled_request_pk PRIMARY KEY (id))''')

db_conn.commit()
db_conn.close()
