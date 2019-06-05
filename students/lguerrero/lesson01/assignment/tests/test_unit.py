import unittest
from unittest.mock import MagicMock, patch

from inventory_management.InventoryClass import Inventory
from inventory_management.FurnitureClass import Furniture
from inventory_management.ElectricAppliancesClass import ElectricAppliances
from inventory_management import main



class InventoryTest(unittest.TestCase):
    """
    InventoryTest class to test 
    """
    def test_inventory(self):

        elect_app1 = {
            'productCode': '001',
            'description': 'elect_1',
            'marketPrice': '$25',
            'rentalPrice': '$15'
        }

        
        self.assertEqual(elect_app1, Inventory('001', 'elect_1', '$25', '$15').return_as_dictionary());



class FurnitureTest(unittest.TestCase):
    """
    FurnitureTest class to test 
    """
    def test_furniture(self):

        elect_app1 = {
            'productCode': '001',
            'description': 'elect_1',
            'marketPrice': '$25',
            'rentalPrice': '$15',
            'material': 'material1',
            'size': 'size1'
        }


        self.assertEqual(elect_app1, Furniture('material1', 'size1', '001', 'elect_1', '$25', '$15').return_as_dictionary());



class ElectricAppliancesTest(unittest.TestCase):
    """
    ElectricAppliancesTest class to test 
    """
    def test_electric_appliances(self):

        elect_app1 = {
            'productCode': '001',
            'description': 'elect_1',
            'marketPrice': '$25',
            'rentalPrice': '$15',
            'brand': 'brand1',
            'voltage': '220v'
        }

        
        self.assertEqual(elect_app1, ElectricAppliances('brand1', '220v', '001', 'elect_1', '$25', '$15').return_as_dictionary());



class MainTests(unittest.TestCase):
    """
    MainTests class to test 
    """
    def test_add_new_item(self):
        """ Test adding new item """
        input_info = ['prod01', 'desc01', '$45', '$65']
        with patch('builtins.input', side_effect=input_info):
            new_item = main.add_new_item()
        self.assertEqual(
            {
                'product_code': 'prod01',
                'description': 'desc01',
                'market_price': '$45',
                'rental_price': '$65'
            },
            new_item)

