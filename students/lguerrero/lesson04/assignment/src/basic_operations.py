from customer_model import *
from playhouse.shortcuts import model_to_dict


# Create a custom logger
LOGGER = logging.getLogger(__name__)

# Create handlers
C_HANDLER = logging.StreamHandler()
F_HANDLER = logging.FileHandler('db.log')
C_HANDLER.setLevel(logging.WARNING)
F_HANDLER.setLevel(logging.INFO)

# Create formatters and add it to handlers
C_FORMAT = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
F_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
C_HANDLER.setFormatter(C_FORMAT)
F_HANDLER.setFormatter(F_FORMAT)

# Add handlers to the logger
LOGGER.addHandler(C_HANDLER)
LOGGER.addHandler(F_HANDLER)




DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')


def add_customer(customer_id,
                 name,
                 last_name,
                 home_address,
                 phone_number,
                 email_address,
                 status,
                 credit_limit):

    """ Inser new customers into the customer
        table customer.db sqlite3 database"""

    LOGGER.info('Adding customer information')

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
            LOGGER.info('Database add successful')

    except Exception as e:
        LOGGER.info('Error creating new customer')
        LOGGER.info(e)
        LOGGER.info('See how the database protects our data')



def search_customer(customer_id):

    """  Returns a dictionary object with name, lastname,
         email address and phone number of a customer
         or an empty dictionary object if no customer was found """

    LOGGER.info(f'Searching customer with customer_id %s', customer_id)

    try:
        return model_to_dict(Customer.select().where(Customer.customer_id == customer_id).get())

    except:
        LOGGER.info(f'Customer witn customer_id %s -- Not found', customer_id)
        return {}



def delete_customer(customer_id):

    """ This function will delete a customer
        from the sqlite3 database """

    try:
        LOGGER.info(f'Deleting instance customer_id: %s', customer_id)
        Customer.get(Customer.customer_id == customer_id).delete_instance()
    except:
        LOGGER.info(f'Customer witn customer_id %s -- Not found', customer_id)



def update_customer_credit(customer_id, credit_limit):

    """ This function will search an existing customer
        by customer_id and update their credit limit
        or raise a ValueError exception if the customer does not exist """  

    if search_customer(customer_id) =={}:
        raise ValueError("Customer No Found")
    else:
        LOGGER.info(f'Update for customer_id: %s credit_limit to %s', customer_id, credit_limit)
        Customer.update(credit_limit = credit_limit).where(Customer.customer_id == customer_id).execute()
        


def list_active_customers(): 

    """ This function will return an integer with
        the number of customers whose status is currently active """
        
    status = ['active', 'Active', 'ACTIVE']
    active_customers = Customer.select().where(Customer.status.in_(status)).dicts()
    return len(active_customers)
