# structs, in Python!
import os

casted_information = {}

def _write_(information_1,information_2 = None):

    # "flushing" the file to be empty

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

        if isinstance(struct_items,list):
            self.StructItems = struct_items
            self.struct_names = self.StructItems
        else:
            if isinstance(struct_items,dict):
                raise Exception('Cannot parse through dictionary')
            if isinstance(struct_items,object):
                raise Exception('Cannot parse through obejct')
            self.StructItems = [struct_items]
            self.struct_names = self.StructItems
        print(self.struct_names)
        self.struct_name_values = []
        self.updated_names = {}
        self.update_values = {}
        self.information = {} # this will hold the struct names and information
        self.current_name_index = 0
        self.current_info_index = 0

        for i in struct_items:
            self.information.update({i:{}})
        
        #for i in struct_items:
            #self.struct_names.append(i)
    
    def _init_items_(self, **kwargs) -> list:

        LIST_OF_ITEMS = []

        for val, item in kwargs.items():
            if val == 'length':
                if isinstance(item,bool):
                    if item == True:
                        LIST_OF_ITEMS.append(len(self.struct_names))
            if val == "dict_":
                if isinstance(item,bool):
                    if item == True:
                        LIST_OF_ITEMS.append(self.information)
            if val == "names":
                if isinstance(item,bool):
                    if item == True:
                        LIST_OF_ITEMS.append(self.struct_names)
            if val == 'all':
                if isinstance(item,bool):
                    if item == True:
                        LIST_OF_ITEMS.append(len(self.struct_names))
                        LIST_OF_ITEMS.append(self.information)
        
        return LIST_OF_ITEMS
    
    def _grab_item_(self,item_type, from_):

        for i in from_:
            if isinstance(i,item_type):
                return i
    
    def _grab_names_(self, not_null=False) -> list:
        
        if not_null == False:
            return self.struct_names
        else:
            items = []
            for i in self.struct_names:
                if self.information[i] == {}:
                    continue
                else: items.append(i)
            
            if len(items) == 0:
                items.append('All struct items are null')
            return items
    
    @CastNewItem(['StructUpdateStructName','Updating struct name'])
    def update_name(self, item_name, item_new_name) -> (dict,None):

        index = 0
        found = False
        info = ''
        for i in range(len(self.struct_names)):
            if item_name == self.struct_names[i]:
                index = i
                found = True
                break

        if found == True:
            self.struct_names[index] = item_new_name
            if self.information[item_name] != {}:
                info = self.information[item_name]
            del(self.information[item_name])
            self.information.update({self.struct_names[index]:info if info else {}})

            if self.update_values:
                if item_name in self.update_values:
                    value = self.update_values[item_name]
                    del(self.update_values[item_name])
                    self.update_values.update({item_new_name:value})

            self.updated_names.update({item_new_name:item_name})
        
            return self.updated_names
    
    @CastNewItem(['StructUpdateStructItemInfo','Updating struct item information/value'])
    def update_value(self, item_name, new_value) -> (dict, None):

        index = 0
        found = False
        for i in range(len(self.struct_names)):
            if item_name == self.struct_names[i]:
                index = 0
                found = True
                break
        
        if found == True:
            if self.struct_name_values[index]:
                self.struct_name_values[index] = new_value
                self.update_values.update({item_name:new_value})
                
                return self.update_values
            else: 
                self.struct_name_values.append(new_value)
                self.current_info_index += 1
            self.information[item_name] = new_value


            return None

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
    def AddInfo(self, Item_Name,Item_Info):

        if isinstance(Item_Name,list):
            if isinstance(Item_Info, list):
                if len(Item_Info) > len(Item_Name):
                    raise Exception('\nCannot assign more values than there are items\n')
                if len(Item_Name) > len(Item_Info):
                    
                    for i in range(len(Item_Name)):
                        if i == len(Item_Info): break

                        if Item_Name[i] in self.information:
                            self.information[Item_Name[i]] = Item_Info[i]
                    
                    if Item_Name[len(Item_Name)-1] in self.information:
                        self.information[Item_Name[len(Item_Name)-1]] = "NULL"
                else:
                    for i in Item_Name:
                        if not i in self.information:
                            raise Exception(f'\nItem {i} not found\n')
                    
                    for i in range(len(Item_Info)):
                        self.information[Item_Name[i]] = Item_Info[i]
            else:
                for i in Item_Name:
                    if i in self.information:
                        self.information[i] = Item_Info
        
        else:
            self.struct_name_values.append(Item_Info)
            if Item_Name in self.information:
                self.information[Item_Name] = self.struct_name_values[self.current_info_index]
            else:
                raise Exception('\nCannot give value to something that does not exist in the struct\n')

            self.current_info_index += 1
    
    @CastNewItem(['PrintingStructItem','Printing the struct item'])
    def print_struct_item(self, item_name, extra = True):

        item = ''
        if isinstance(item_name,list):
            for i in item_name:
                if i in self.information:
                    if self.information[i] == {}:
                        self.information[i] = "NULL"
                    if i in self.updated_names and extra == True:
                        item = i + '(UPDATED)'
                    else: item = i
                    print(item+':\t',self.information[i])
        else:
            if item_name in self.information:
                if item_name in self.updated_names and extra == True:
                    item_name = item_name + '(UPDATED)'
                print(item_name+':\t',self.information[item_name])
    
    @CastNewItem(['PrintAllItems','Printing all Struct items'])
    def print_all(self, extra = True):

        tabs = 0
        tabs_ = ''
        curr = 0
        all = []
        item_to_tab = ''

        for i in self.information:
            all.append(i)
            if self.information[i] == {}:
                self.information[i] = "NULL"
    
        for i in range(len(all)):
            if i > 1:

                if len(all[i-1]) > len(all[i]):
                    item_to_tab = all[i]
                    tabs = len(all[i-1])-len(all[i])+1
                    tabs_ = ' '*tabs

        item = ''
        item_info = ''
        for i in all:
            if i in self.updated_names and extra == True:item = i + '(UPDATED)'
            else: item = i

            if i in self.update_values and extra == True:item_info = self.update_values[i] + '(UPDATED)'
            else: item_info = self.information[i]

            if i == item_to_tab:
                print(item+f':\t{tabs_}',item_info)
            else: print(item+':\t',item_info)

            curr += 1
