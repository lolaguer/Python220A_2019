'''
This module describes the Furniture class
'''

from inventory_management.InventoryClass import Inventory

#from inventory_class import Inventory

class Furniture(Inventory):
    '''
    Furniture class
    '''

    def __init__(self, material, size, *args):
        # Creates common instance variables from the parent class
        super().__init__(*args)
        self.material = material
        self.size = size

    def return_as_dictionary(self):
        '''
        Return a dictionary
        '''

        output_dict = super().return_as_dictionary()
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
