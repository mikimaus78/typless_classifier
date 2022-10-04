#!/usr/bin/python
import logging
import sqlite3
from datetime import datetime

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('DB')

DATABASE_PATH = './database/algoritmik.db.db'

def create_database():
    conn = sqlite3.connect(DATABASE_PATH)
    logger.info("Opened database successfully")

    conn.execute('''CREATE TABLE docsys 
           (id INTEGER PRIMARY KEY AUTOINCREMENT, 
           supplier_name   TEXT    NOT NULL, 
           invoice_number  INT     NOT NULL, 
           issue_date  INT         NOT NULL, 
           pay_due_date INT        NOT NULL, 
           total_amount         REAL);''')
    logger.info("Table created successfully")
    conn.close()


def insert_record(data):
    conn = sqlite3.connect(DATABASE_PATH)
    logger.info("Opened database successfully")

    insert_stm = "INSERT INTO docsys (supplier_name, invoice_number, issue_date, pay_due_date, total_amount ) " \
                 "VALUES ( '{0}', {1}, {2}, {3}, {4} )"\
        .format(data['supplier_name'], data['invoice_number'], data['issue_date'], data['pay_due_date'], data['total_amount'])
    conn.execute(insert_stm)

    conn.commit()
    logger.info("Record successfully inserted!")


if __name__ == '__main__':
    create_database()
