#encoding:utf-8

import configparser as ConfigParser
import os
import platform

class Config:
    '''
        This is the config class for user to get the database information.
        \n- You should put the config.ini file in the same folder with this python script
        \n- Included functions as below:
            \n-> get_config_version()
            \n-> get_config_db_info()
    '''
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        #file_path = ".."+os.sep+"config"+os.sep+"config.ini" # 用os.sep来实现跨平台, config.ini文件要在同一个文件夹下
        file_path = os.path.dirname(os.path.realpath(__file__))+os.sep+'..'+os.sep+"config"+os.sep+"config.ini" # 用os.sep来实现跨平台, config.ini文件要在同一个文件夹下
        self.is_file_exist = True
        
        if os.path.exists(file_path):
            self.cf.read(file_path)
        else:
            self.is_file_exist = False
            print("config.ini file doesn't exist!")
    
    def get_config_version(self):
        '''
        This method is for user to get the version of the config program
        '''
        
        if self.is_file_exist == False:
            print("Error: Cannot get the version value!")
            return
        
        str_version = self.cf.get("version","version") #获取版本信息
        return str_version
    
    def get_config_db_info(self):
        '''
        This method is for user to get the database info which is stored in the config.ini file
        '''
        if self.is_file_exist == False:
            print("Error: Cannot get the database value!")
            return
        
        db_items = self.cf.options("db") #判断信息是否足够
        if 'db_host' not in db_items:
            print("please input db_host in the config.ini file")
            raise IOError
        elif 'db_port' not in db_items:
            print("please input db_port in the config.ini file")
            raise IOError
        elif 'db_user' not in db_items:
            print("please input db_user in the config.ini file")
            raise IOError
        elif 'db_pass' not in db_items:
            print("please input db_pass in the config.ini file")
            raise IOError
        #elif 'db_name' not in db_items:
            #print("please input db_name in the config.ini file")
            #raise IOError
        
        #数据库的基本信息 
        db_host = self.cf.get("db","db_host")
        db_port = self.cf.get("db","db_port")
        db_user = self.cf.get("db","db_user")
        db_pass = self.cf.get("db","db_pass")
        #db_name = self.cf.get("db","db_name")
        return {'host':db_host,
                'port':db_port,
                'user':db_user,
                'pass':db_pass,
                #'name':db_name
                }
                        

if __name__=='__main__':
    test = Config()
    version=test.get_config_version() #get the version
    db = test.get_config_db_info()
    print('version:'+version)
    #print('db:',db)
    print('db_host',db['host'])
    