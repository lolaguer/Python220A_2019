from customer_model import *
from playhouse.shortcuts import model_to_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')


def add_customer(customer_id, name, last_name, home_address, phone_number, email_address, status, credit_limit):

    """ Inser new customers into the customer table customer.db sqlite3 database"""

    logger.info('Adding customer information')

    try:
        with DATABASE.transaction():
            new_customer = Customer.create(
                            customer_id=customer_id,
                            name=name,
                            last_name=last_name,
                            home_address=home_address,
                            phone_number=phone_number,
                            email_address=email_address,
                            status=status,
                            credit_limit=credit_limit)
            new_customer.save()
            logger.info('Database add successful')

    except Exception as e:
        logger.info('Error creating new customer')
        logger.info(e)
        logger.info('See how the database protects our data')



def search_customer(customer_id):

    """  Returns a dictionary object with name, lastname, email address and phone number of a customer 
         or an empty dictionary object if no customer was found """

    logger.info(f'Searching customer with customer_id %s', customer_id)

    try:
        return model_to_dict(Customer.select().where(Customer.customer_id == customer_id).get())

    except Exception as e:
        logger.info(f'Customer witn customer_id %s -- Not found', customer_id)
        return {}



def delete_customer(customer_id):

    """ This function will delete a customer from the sqlite3 database """

    try:
        logger.info(f'Deleting instance customer_id: %s', customer_id)
        Customer.get(Customer.customer_id == customer_id).delete_instance()
    except Exception as e:
        logger.info(f'Customer witn customer_id %s -- Not found', customer_id)



def update_customer_credit(customer_id, credit_limit): 

    """ This function will search an existing customer by customer_id and update their credit limit
        or raise a ValueError exception if the customer does not exist """  

    if search_customer(customer_id) =={}:
        raise ValueError("Customer No Found")
    else:
        logger.info(f'Update for customer_id: %s credit_limit to %s', customer_id, credit_limit)
        Customer.update(credit_limit = credit_limit).where(Customer.customer_id == customer_id).execute()
        


def list_active_customers(): 

    """ This function will return an integer with the number of customers
        whose status is currently active """
    status = ['active', 'Active', 'ACTIVE']
    active_customers = Customer.select().where(Customer.status.in_(status)).dicts()
    return len(active_customers)
