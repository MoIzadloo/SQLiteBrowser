import os
import sqlite3


class sqlite():

    '''
    ###############################

    This class will help you with sqlite3 lib 
    And automate many things for an easier user
    Interface

    dbName = the name of database file (str)

    ###############################
    '''

    def __init__(self,dbPath):
        self.dbPath = dbPath
        self.__conn = sqlite3.connect(self.dbPath) 
        self.__c = self.__conn.cursor()

    def conn_commit(self):
        '''
        ###############################

        This method will call commit method after each successful 
        Sql command, its necessary to call commit method


        ###############################
        '''
        self.__conn.commit()

    def reflectorArgs(self,args):
        '''
        ###############################

        This method will get args and return a string
        In a special format 

        " 
            "text , "text" , integer ...

        "

        ###############################
        '''
        output = ''
        for arg in args:
            if arg != args[-1]:
                if isinstance(arg , int):
                    output = output + f'{arg}' + " , "
                elif isinstance(arg , str):
                    output = output + f'"{arg}"' + " , "
            else:
                if isinstance(arg , int):
                    output = output + f'{arg}' 
                elif isinstance(arg , str):
                    output = output + f'"{arg}"' 

        return output
        
    def reflectorKwargsH(self,kwargs):
        '''
        ###############################

        This method will get kwargs and split key and value 
        Into two different lists then make an string in a
        Special format 

        " 
        key = "value" AND key = "value" ...
        "

        ###############################
        '''

        name = []
        type = []
        output = ''
        for key in kwargs.keys():
            name.append(key)
        for value in kwargs.values():
            type.append(value)    
        for x in range(len(name)):
            if x != len(name) - 1:
                output = (output + name[x] + ' = ' + f'"{type[x]}"' + ' AND ')
            else:
                output = (output + name[x] + ' = ' + f'"{type[x]}"')
        return output

    def reflectorKwargsV(self,kwargs):
        '''
        ###############################

        This method will get kwargs and split key and value 
        Into two different lists then make an string in a
        Special format 

        "key value,
         key value,
         key value,
         ..."

        ###############################
        '''
        name = []
        type = []
        output = ''
        for key in kwargs.keys():
            name.append(key)
        for value in kwargs.values():
            type.append(value)    
        for x in range(len(name)):
            if x != len(name) - 1:
                output = (output + name[x] + ' ' + type[x] + ',\n')
            else:
                output = (output + name[x] + ' ' + type[x])
        return output

    def execute_manuall(self,command,fetch = 'all'):
        '''
        ###############################

        This method will allow you to execute your manuall
        Sql command

        Example : db.execute_manuall("SELECT * FROM tablename")

        ###############################
        '''
        self.__c.execute(command)
        self.conn_commit()
        if fetch == 'all':
            return self.__c.fetchall()
        elif fetch == 'one':
            return self.__c.fetchone()
        elif 'many' in fetch:
            return self.__c.fetchmany(fetch[1])
        
    def createTable(self,tbName,**kwargs):
        '''
        ###############################

        This method will create a table with name and columns that
        Comes from tbName(str) and **kwargs(dict) if table is not exists already

        Example : db.createTable('projects' , id = 'integer PRIMARY KEY' , name = 'text NOT NULL')

        ###############################
        '''
        columns = self.reflectorKwargsV(kwargs)
        self.__c.execute(f'CREATE TABLE IF NOT EXISTS {tbName} ({columns})')
        self.conn_commit()

    def insertInto(self,tbName,*args):
        '''
        ###############################

        This method will insert values into columns of a specific table

        Example : db.insertInto('employe' , 'jack' , 'Acton' , 3000)

        ###############################
        '''
        inputs = self.reflectorArgs(args)
        self.__c.execute(f'INSERT INTO {tbName} VALUES ({inputs})')
        self.conn_commit()

    def selectAll(self,tbName,fetch = 'all'):
        '''
        ###############################

        This method will select and fetch (all,one,many) all values in columns of a specific table

        Example : db.insertInto('employe', fetch =('many' , 2))

        ###############################
        '''
        self.__c.execute(f'SELECT * FROM {tbName}')
        self.conn_commit()
        if fetch == 'all':
            return self.__c.fetchall()
        elif fetch == 'one':
            return self.__c.fetchone()
        elif 'many' in fetch:
            return self.__c.fetchmany(fetch[1])

    def selectAllFrom(self,tbName,fetch = 'all',**kwargs):
        '''
        ###############################

        This method will select and fetch (all,one,many) all values in all columns of a specific table where 
        Have true information

        Example : db.selectAllFrom('employe', fetch = 'all' , last = 'Acton')

        ###############################
        '''
        column = ''
        value = ''
        for key in kwargs.keys():
            column = key
        for var in kwargs.values():
            value = var
        self.__c.execute(f'SELECT * FROM {tbName} WHERE {column} = "{value}"')
        self.conn_commit()
        if fetch == 'all':
            return self.__c.fetchall()
        elif fetch == 'one':
            return self.__c.fetchone()
        elif 'many' in fetch:
            return self.__c.fetchmany(fetch[1])

    def selectValueFrom(self,tbName,*args,fetch = 'all',**kwargs):
        '''
        ###############################

        This method will select and fetch (all,one,many) specific values in specific columns of a specific table where 
        Have true information

        Example : db.selectAllFrom('employe', 'last' , 'first' , fetch = 'all' , last = 'Acton' )

        ###############################
        '''
        output = self.reflectorArgs(args).replace('"' , '' )
        column = ''
        value = ''
        for key in kwargs.keys():
            column = key
        for var in kwargs.values():
            value = var
        self.__c.execute(f'SELECT {output} FROM {tbName} WHERE {column} = "{value}"')
        self.conn_commit()
        if fetch == 'all':
            return self.__c.fetchall()
        elif fetch == 'one':
            return self.__c.fetchone()
        elif 'many' in fetch:
            return self.__c.fetchmany(fetch[1])

    def dropTable(self,tbName):
        '''
        ###############################

        This method will remove table from database if table is exists

        Example : db.dropTable('employe')

        ###############################
        '''
        self.__c.execute(f'DROP TABLE IF EXISTS {tbName}')
        self.conn_commit()

    def delete(self,tbName,**kwargs):
        '''
        ###############################

        This method will remove values from database if the informations
        Are correct

        Example : db.delete('employe' , Elast = 'Acton' )

        ###############################
        '''
        output = self.reflectorKwargsH(kwargs)
        self.__c.execute(f'DELETE FROM {tbName} Where {output}')
        self.__conn.commit()


    def show_tables(self):
        self.__c.execute('SELECT tbl_name from sqlite_master')
        self.conn_commit()
        return self.__c.fetchall()


    
        

