from unittest import TestCase
from unittest.mock import MagicMock, patch

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances



class InventoryTest(unittest.TestCase):

    def test_inventory(self):

        elect_app1 = {
            product_code: '001',
            description: 'elect_1',
            market_price: '$25',
            rental_price: '$15'
        }

        
        self.assertEqual(elect_app1, Inventory('001', 'elect_1', '$25', '$15'));



class FurnitureTest(unittest.TestCase):

    def test_furniture(self):

        elect_app1 = {
            product_code: '001',
            description: 'elect_1',
            market_price: '$25',
            rental_price: '$15',
            material: 'material1',
            size: 'size1'
        }

        
        self.assertEqual(elect_app1, Furniture('001', 'elect_1', '$25', '$15', 'material1', 'size1'));



class ElectricAppliancesTest(unittest.TestCase):

    def test_electric_appliances(self):

        elect_app1 = {
            product_code: '001',
            description: 'elect_1',
            market_price: '$25',
            rental_price: '$15',
            brand: 'brand1',
            voltage: '220v'
        }

        
        self.assertEqual(elect_app1, ElectricAppliances('001', 'elect_1', '$25', '$15', 'brand1', '220v'));