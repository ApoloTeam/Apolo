#encoding:utf-8
import pandas as pd
from modules import db_connector

DB = db_connector.Db_connector()
    
DB.update_db_dividend_data()
