# structs, in Python!
import os

casted_information = {}

def _write_(information_1,information_2 = None):

    # "flushing" the file to be empty
    os.remove('info.txt')

    with open('info.txt','w') as file:

        file.write(information_1+'\n')
        if not information_2 == None:
            file.write('\n'+information_2)
        file.flush()
        file.close()

class CastNewItem(object):

    def __init__(self, new_information):

        if len(new_information) > 1:
            self.new_item_name = new_information[0]
            self.new_item_info = new_information[1]
        else: raise Exception('\nCannot Cast item without item information\n')

        self.InformationToWrite = ''
    
    def __call__(self, func):

        self.InformationToWrite = 'Casted Struct Item Name: %s\nCasted Struct Item %s Value/Info: \n\t%s'

        if not os.path.isfile('info.txt'):
            _write_(self.InformationToWrite % (self.new_item_name,self.new_item_name,self.new_item_info))
        
        else:

            old_info = open('info.txt','r').read()
            if not self.new_item_name in old_info or not self.new_item_info in old_info:
                _write_(self.InformationToWrite % (self.new_item_name,self.new_item_name,self.new_item_info),old_info)
            
            #else: _write_(self.new_item_name,self.new_item_info)

        return func

class CreateStruct:

    def __init__(self, struct_items):

        self.StructItems = struct_items
        self.struct_names = []
        self.struct_name_values = []
        self.information = {} # this will hold the struct names and information
        self.current_name_index = 0
        self.current_info_index = 0

    @CastNewItem(['NewStructItem','Adding new Struct item'])
    def add_items(self, struct_item_name, add_many = 0):

        # if struct_item_name is a list
        if add_many > 0:
            for i in add_many:
                self.struct_names.append(struct_item_name[i])
                self.information.update({self.struct_names[self.current_name_index]:{}})

                self.current_name_index += 1
        else:
            self.struct_names.append(struct_item_name)
            self.information.update({self.struct_names[self.current_name_index]:{}})

            self.current_name_index += 1

    @CastNewItem(['NewStructItemInformation', 'Adding struct item value/information'])
    def __init_struct_item_info_(self, struct_item_info):
        self.struct_name_values.append(struct_item_info)
        self.information[self.struct_names[self.current_info_index]] = self.struct_name_values[self.current_info_index]

        self.current_info_index += 1

STRUCT = CreateStruct(['ItemOne','ItemTwo','ItemThree'])
STRUCT.add_items('hey')