'''
Electric appliances class
'''

from inventory_management.InventoryClass import Inventory

#from inventory_class import Inventory

class ElectricAppliances(Inventory):
    '''
    Creates objects with appliances characteristics
    '''

    def __init__(self, brand, voltage, *args):
        #Creates common instance variables from the parent class
        super().__init__(*args)
        self.brand = brand
        self.voltage = voltage

    def return_as_dictionary(self):
        '''
        Return dictionary
        '''

        output_dict = super().return_as_dictionary()
        output_dict['brand'] = self.brand
        output_dict['voltage'] = self.voltage

        return output_dict
