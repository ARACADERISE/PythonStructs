# structs, in Python!
import os, json

"""
    That one powerful Python tool to work with data..that only used/imported two ies for only one use: checking if a single file existed/loading stringified dictionaries

    Users Note:
        The application is only capable of parsing 2d arrays/dictionary arrays.
        Anything beyond that it will then "link" the arrays
"""

casted_information = {}

def _write_(information_1,information_2 = None):

    # "flushing" the file to be empty
    if os.path.exists('info.txt'):
        flush = open('info.txt','w')
        flush.write('')
        flush.close()

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
        
        # declared before if statements
        self.file_storage_name = None
        self.struct_name_values = []
        self.struct_names = []
        self.StructItems = []
        self.information = {}
        self.current_name_index = 0
        self.current_info_index = 0
        if isinstance(struct_items,list):
            self.StructItems = struct_items
            self.struct_names = self.StructItems
        else:
            if isinstance(struct_items,dict):
                for i in struct_items:
                    self.StructItems.append(i)
                    self.struct_names = self.StructItems
                    self.struct_name_values.append(struct_items[i])
                    self.information.update({i:struct_items[i]})
                    
        self.updated_names = {}
        self.update_values = {}

        if self.information == {}:
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
            if val == 'values':
                if isinstance(item,bool):
                    if item == True:
                        # Quickly filtering the self.struct_name_values list for repetition
                        # START {
                        al_ = []
                        for i in self.struct_name_values:
                            if isinstance(i,list):
                                for x in i:
                                    if not x in al_:
                                        al_.append(x)
                            else:
                                al_.append(i)
                        self.struct_name_values = al_
                        # } END
                        LIST_OF_ITEMS.append(self.struct_name_values)
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
    
    def reload_info(self):

        if self.file_storage_name:
            
            self.information = json.loads(open(self.file_storage_name,'r').read())
            
            self.current_info_index = 0
            self.current_name_index = 0
            self.struct_name_values = []
            self.struct_names = []
            self.StructItems = []

            for i in self.information:

                self.StructItems.append(i)
                self.struct_names = self.StructItems

                if isinstance(self.information[i],list):
                    for x in self.information[i]:
                        self.struct_name_values.append(x)

                self.current_name_index += 1
                self.current_info_index += 1
    
    def _grab_item_(self,item_type, from_):
        
        if from_ in self.struct_names:
            from_ = self.information[from_]
        else:
            raise Exception(f'{from_}' does not exist')
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
    
    @CastNewItem(['StructDeleteItem','Deleting an item from the struct'])
    def delete_item(self, item_name) -> (dict or None):

        if item_name in self.struct_names:
            index = 0
            for i in range(len(self.struct_names)):
                if self.struct_names[i] == item_name:
                    index = i
                    break

            del(self.struct_names[index])

            # Wrapping it in try:except to avoid any errors
            try:
                del(self.struct_name_values[index])
            except: pass
            if item_name in self.information:
                del(self.information[item_name])

                return self.information
            else:
                raise Exception('Item does not exist')

    @CastNewItem(['StructUpdateStructName','Updating struct name'])
    def update_name(self, item_name, item_new_name) -> (dict or None):

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
    def update_value(self, item_name, new_value) -> (dict or None):

        if item_name in self.struct_names:
            index = 0
            for i in range(len(self.struct_names)):

                if self.struct_names[i] == item_name:
                    index = i
                    break
            
            self.struct_name_values[index] = new_value

            if item_name in self.information:
                self.information[item_name] = self.struct_name_values[index]

                return self.information
            else:
                raise Exception('Item does not exist')


    @CastNewItem(['NewStructItem','Adding new Struct item'])
    def add_items(self, struct_item_name, add_many = 0):

        # if struct_item_name is a list
        if add_many > 0:
            for i in range(add_many):
                if not struct_item_name[i] in self.struct_names:
                    self.struct_names.append(struct_item_name[i])
                    self.information.update({struct_item_name[i]:{}})

                    self.current_name_index += 1
        elif isinstance(struct_item_name,list):
            for i in struct_item_name:
                if isinstance(i,list):
                    for x in i:
                        if not x in self.struct_names:
                            self.struct_names.append(x)
                            self.information.update({x:{}})
                            self.current_name_index += 1
                else:
                    if not i in self.struct_names:
                        self.struct_names.append(i)
                        self.information.update({i:{}})
                        self.current_name_index += 1
        else:
            if not struct_item_name in self.struct_names:
                self.struct_names.append(struct_item_name)
                self.information.update({struct_item_name:{}})

                self.current_name_index += 1
    
    @CastNewItem(['StructAppend','Appending one struct to another'])
    def _save_(self, file = 'information.json',extra_info = None) -> (list or dict):
        to_write = self.information
        if not extra_info == None:
            if extra_info[0]:
                to_write.update({'extra_saved_items':extra_info[0]})
            else: to_write.update({'extra_saved_info':extra_info})
        
        to_write = str(to_write).replace("'",'"')

        if self.file_storage_name == None:
            self.file_storage_name = file
        with open(self.file_storage_name,'w') as file:
            file.write(to_write)
            file.close()
        
        return self.information
    
    def _storage_file_(self): return self.file_storage_name

    @CastNewItem(['NewStructItemInformation', 'Adding struct item value/information'])
    def AddInfo(self, Item_Name,Item_Info):

        secondary_index = 0
        if isinstance(Item_Name,list):
            if isinstance(Item_Info, list):
                if len(Item_Info) > len(Item_Name):
                    raise Exception('\nCannot assign more values than there are items\n')
                if len(Item_Name) > len(Item_Info):
                    for i in range(len(Item_Name)):
                        if i == len(Item_Info): 
                            secondary_index = 0
                            break

                        if Item_Name[i] in self.information:
                            if isinstance(Item_Info[i],list):
                                if isinstance(self.information[Item_Name[i]],list):
                                    self.information[Item_Name[i]].append(Item_Info[i][secondary_index])
                                else: self.information[Item_Name[i]] = Item_Info[i][secondary_index]
                                secondary_index += 1
                            else:
                                self.information[Item_Name[i]] = Item_Info[i]
                    
                    if Item_Name[len(Item_Name)-1] in self.information:
                        if isinstance(self.information[Item_Name[len(Item_Name)-1]],list):
                            self.information[Item_Name[len(Item_Name)-1]].append("NULL")
                        else: self.information[Item_Name[len(Item_Name)-1]] = "NULL"
                else:
                    if isinstance(Item_Name[0],list):
                        Item_Name = Item_Name[0]
                    for i in Item_Name:
                        if not i in self.information:
                            raise Exception(f'\nItem {i} not found\n')
                    
                    for i in range(len(Item_Info)):
                        if isinstance(Item_Info[i],list):
                            if isinstance(self.information[Item_Name[i]],list):
                                self.information[Item_Name[i]].append(Item_Info[i][secondary_index])
                            else:
                                self.information[Item_Name[i]] = Item_Info[i][secondary_index]
                            secondary_index += 1
                        else: self.information[Item_Name[i]] = Item_Info[i]
            else:
                for i in Item_Name:
                    if i in self.information:
                        self.information[i] = Item_Info
        elif isinstance(Item_Info,list):
            for i in range(len(Item_Info)):
                if isinstance(self.information[Item_Name],list):
                    if isinstance(Item_Info[i],list):
                        self.information[Item_Name].append(Item_Info[i][secondary_index])

                        secondary_index += 1
                    else: self.information[Item_Name].append(Item_Info[i])
                else:
                    if not self.information[Item_Name] == {} and not self.information[Item_Name] == "NULL":
                        info = [self.information[Item_Name],Item_Info[i]] 
                        self.information[Item_Name] = info
                    else: self.information[Item_Name] = Item_Info[i]
        else:
            if not Item_Info in self.struct_name_values:
                self.struct_name_values.append(Item_Info)

            if Item_Name in self.information:
                if isinstance(self.information[Item_Name],list):
                    self.information[Item_Name].append(Item_Info)
                else:
                    if not self.information[Item_Name] == {} and not self.information[Item_Name] == "NULL":
                        info = [self.information[Item_Name],Item_Info]
                        self.information[Item_Name] = info
                    else:
                        self.information[Item_Name] = self.struct_name_values[self.current_info_index]
                    self.current_info_index += 1
            else:
                raise Exception(f'\nCannot give value to something that does not exist in the struct\n\n')
    
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
        ind = 0
        is_dict = False
        for i in all:
            if i in self.updated_names and extra == True:item = i + '(UPDATED)'
            else: item = i

            if i in self.update_values and extra == True:item_info = self.update_values[i] + '(UPDATED)'
            else: item_info = self.information[i]

            if isinstance(self.information[i],list):
                for x in range(len(self.information[i])):

                    if isinstance(self.information[i][x],dict):

                        ind += 1

                        if ind == len(self.information[i])-1:
                            is_dict = True
                            break
            
            info = []
            it_ = 0
            if is_dict == True:
                for i in self.information:
                    if it_ == 0:
                        info.append(self.information[i][0])
                        it_ += 1
                            
                    for x in range(len(self.information[i])):
                        if not self.information[i][x] in info:
                            info[0].update(self.information[i][x])

            if i == item_to_tab:
                if info: print(item+f':\t{tabs_}',info)
                else: print(item+f':\t{tabs_}',item_info)
            else:
                if info:print(item+':\t',info[0])
                else: print(item+':\t',item_info)

            curr += 1
