#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 2019

@author (comments): Lola Guerrero
"""

""""
must use 127.0.0.1 on windows

"""

from pymongo import MongoClient
import csv
import json
import logging


logger = logging.getLogger("hp_norton_mongodb")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class MongoDBConnection():
    """
     MongoDB Connection
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)



mongo = MongoDBConnection()


# 1 - Create a product database with attributes that reflect the contents of the csv file.
with mongo: #Context manager.
    hp_norton_db = mongo.connection.hp_norton_db
    logger.info("Connected to hp_norton_db database") 

    customers_col = hp_norton_db["customers"]
    product_col = hp_norton_db["product"]
    rental_col = hp_norton_db["rental"]
    logger.info("Customer, product, and rental collections created") 


    # 2 - Import all data in the csv files into your MongoDB implementation.
    # Customer
    f = open( "../data/customers.csv", 'r' )   
    reader = csv.DictReader( f.readlines()[1:], fieldnames = ( "user_id", "name", "address", "zip_code", "phone_number", "email"))  
    out_customer = [json.loads(json.dumps(row)) for row in reader]
    customers_col.insert_many(out_customer)
    logger.info("Insert data from customers.csv file to Customer collection") 

    # Product
    f = open( "../data/product.csv", 'r' )   
    reader = csv.DictReader( f.readlines()[1:], fieldnames = ( "product_id", "description", "product_type", "quantity_available"))  
    out_product = [json.loads(json.dumps(row)) for row in reader]
    product_col.insert_many(out_product)
    logger.info("Insert data from product.csv file to Product collection") 

    # Rental
    f = open( "../data/rental.csv", 'r' )   
    reader = csv.DictReader( f.readlines()[1:], fieldnames = ( "product_id", "user_id"))  
    out_rental = [json.loads(json.dumps(row)) for row in reader]
    rental_col.insert_many(out_rental)
    logger.info("Insert data from rental.csv file to Rental collection") 

    
    
    # 3 - Write queries to retrieve the product data.
    # Get info about a especific product_id:
    def get_product_info(prod_id):

        query_product = {"product_id": prod_id}
        look_product = product_col.find(query_product)

        for prod in look_product:
            print ('Description:', prod['description'])
            print ('Product type:', prod['product_type'])
            print ('Quantity Available:', prod['quantity_available'])

    

    # How many clients has rental an especific product_id:
    def clients_rented_product_info(prod_id):

        query_product = {"product_id": prod_id}
        look_product = rental_col.find(query_product)

        client_ids = []
        for prod in look_product:
            client_ids.append(prod['user_id'])
            print ('Number the clients rented ' + prod_id + ' :', len(client_ids))
            print (client_ids)


    # How many products of each type we have:
    agr = [{'$group': {'_id': "$product_type", "count":{"$sum":1}}}]
    list(product_col.aggregate(agr))

    # How can you change the type of variables???
    agr = [{'$group': {'_id': "$product_type", 'all': { '$sum': '$quantity_available'}}}]
    list(product_col.aggregate(agr))
    

    # 4 - Write a query to integrate customer and product data.
    for CustomerRecord in customers_col.find():
        query = {"user_id": CustomerRecord["user_id"]}
        for rental_id in rental_col.find(query): 
            query = {"product_id": rental_id["product_id"]}
            for product_id in product_col.find(query):
                print(f'Customer: {CustomerRecord["user_id"]} is related to')
                print ('Description:', product_id['description'])
                print ('Product type:', product_id['product_type'])
                print ('Quantity Available:', product_id['quantity_available'])


if __name__ == "__main__":

    print_mdb_collection(customers_col) #Prints all records from customer table
    print_mdb_collection(product_col) #Prints all records from product table
    print_mdb_collection(rental_col) #Prints all records from rental table

    # Queries for product
    get_product_info("prd001") 
    get_product_info("prd002")
    get_product_info("prd003")

    clients_rented_product_info("prd001")
    clients_rented_product_info("prd002")
    clients_rented_product_info("prd003")
    
