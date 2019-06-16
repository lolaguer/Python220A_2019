# Model Definition

from peewee import *
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


DATABASE = SqliteDatabase('customers.db')

class Customer(Model):
    customer_id = CharField(primary_key=True)
    name = CharField(max_length=20)
    last_name = CharField(max_length=20)
    home_address = CharField(max_length=100)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=30)
    status = CharField(max_length=10)
    credit_limit = CharField(max_length=10)

    class Meta:
        database = DATABASE

LOGGER.info('Connect to customers.db')
DATABASE.connect()

LOGGER.info('Create table Customer')
DATABASE.create_tables([Customer])

LOGGER.info('Closecustomers.db')
DATABASE.close()



########################################################################################
#### Importing csv file from data into db (comment it after running the first time) ####
########################################################################################

import csv, sqlite3, codecs

CON = sqlite3.connect("customers.db")
CUR = CON.cursor()

to_db = []
with open('../data/customer.csv','rb') as cus: 
    fcus = csv.reader(codecs.iterdecode(cus, 'utf-8', errors='ignore'))
    for ri, r in enumerate(fcus):
        if ri == 0:
            continue
        else:
            to_db.append(tuple(r))

CUR.executemany("INSERT INTO Customer VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
CON.commit()
CON.close()




