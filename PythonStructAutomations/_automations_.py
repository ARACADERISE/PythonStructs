import sys, os, json

print(os.getcwd())
sys.path.append('../')
try:
    from ..main import CreateStruct
except ImportError:
    raise ImportError('For some unkown reason, CreateStruct cannot be imported from main.')

class StructConnect:

    def __init__(self, file_to_connect_to):

        if file_to_connect_to:
            self.file_to_connect_to = file_to_connect_to
            self.information = json.loads(open(file_to_connect_to,'r').read())

            self.StructConnection = CreateStruct(self.information)
        else:
            raise Exception('No file to connect to')
    
    def __init_item__(self): return self.StructConnection
    def _file_name_(self): return self.file_to_connect_to

class EntitleDb(object):

    def __init__(self, object, file_name):

        self.db = object
        self.conn_name = file_name
        self.db_information = {'Inserts':[None],'Commits':[None]} # storing all information
        self.current_updated_name = ''
        self.current_update_value = ''

    def insert(self, item_name, item_info):
    
        self.db.AddInfo(item_name,item_info)

        if None in self.db_information['Inserts']:
            del(self.db_information['Inserts'][0])
    
        self.db_information['Inserts'].append({'New_Value':{'to':item_name,'new value':item_info}})

        self.current_updated_name = item_name
        self.current_update_value = item_info
    
    def _grab_(self, item_name) -> list:

        names = self.db._grab_names_()
        values = self.db._init_items_(dict_=True)[0]
        return_list = []
        
        if item_name in names:

            index = 0
            for i in range(len(names)):

                if names[i] == item_name:
                    index = i
                    break
            
            return_list.append({names[index]:values[item_name]})

            return return_list
    
    def _delete_(self, item_name):

        op = json.loads(open(self.conn_name,'r').read())

        if item_name in op:

            self.db.delete_item(item_name)
            
            del(op[item_name])
            with open(self.conn_name, 'w') as file:
                file.write(json.dumps(
                    op,
                    indent=2,
                    sort_keys=False
                ))
                file.close()
    
    def _commit_change_(self):

        if None in self.db_information['Commits']:
            del(self.db_information['Commits'][0])
        
        information = self.db._init_items_(values=True)[0]
        
        self.db_information['Commits'].append({'Commited_Changes':{'to':self.current_updated_name,'value':information}})

        with open('db.json','w') as file:
            file.write(
                json.dumps(
                    self.db_information,
                    indent=2,
                    sort_keys=False
                )
            )
            file.close()
        
        with open(self.conn_name,'w') as file:
            file.write(json.dumps(
                self.db._init_items_(dict_=True)[0],
                sort_keys=False
            ))
            file.close()
    
    def _select_(self, item = None, as_='values'):

        names = self.db._init_items_(names=True)[0]
        information = self.db._init_items_(dict_=True)[0]

        if not item == None and item in names:

            if as_ == 'values':
                return information[item]
            elif as_ == 'names':
                info = self.db._init_items_(names=True)[0]

                info_ = []
                for i in info:
                    if i in information[item]:
                        info_.append(i)
                
                return info_
            elif as_ == 'all':
                return self.db._init_items_(names=True)[0],self.db._init_items_(values=True)[0]
        elif item == None:
            if as_ == 'all':
                return self.db._init_items_(all=True)
            elif as_ == 'values':
                return self.db._init_items_(values=True)[0]
            else:
                if as_ == 'names':
                    return self.db._init_items_(names=True)[0]
