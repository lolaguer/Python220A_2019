'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging

LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+'_charges_calc.log'
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler(LOG_FILE)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()

def parse_cmd_arguments():
    ''' Argumantes to pass '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', help='Debug level: 0:info, 1: error, 2: warn, 3: debug', default=0, required=False)
    return parser.parse_args()


def load_rentals_file(filename):
    ''' Loads rentals file data '''
    with open(filename) as file:
        try:
            LOGGER.info('loading JSON file %s', filename)
            return json.load(file)
        except ValueError as err:
            LOGGER.error('Failed to load JSON data: %s', err)
            exit(0)


def calculate_additional_fields(d_data):
    ''' Calculates additional fields '''
    LOGGER.info('Calculating additional fields')

    for value in d_data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
        except ValueError as err:
            LOGGER.warning("Failed to calculate time from %s or %s. ERROR: %s", value['rental_start'], value['rental_end'], err)
            continue



        if rental_start >= rental_end:
            LOGGER.warning("Rental starts %s on or after ends %s in %s.  Skip.", rental_start, rental_end, value)
            continue

        try:
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except Exception as err:
            LOGGER.error('Failed Calculating additional fields: %s', err)
            exit(0)

    return d_data

def save_to_json(filename, data):
    ''' Save to json '''
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    DATA = load_rentals_file(ARGS.input)
    DATA1 = calculate_additional_fields(DATA)
    save_to_json(ARGS.output, DATA1)
