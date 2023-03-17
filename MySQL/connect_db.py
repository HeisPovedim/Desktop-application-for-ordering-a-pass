import mysql.connector
from .config import *

class DB(object):
  def __init__(self):
    self.connect = mysql.connector.connect(
      host = host,
      user = user,
      password = password,
      database = database
    )
    
    self.cursor = self.connect.cursor()
    
    if self.connect.is_connected():
      print("Connected to MySQL Database")
    else:
      print("Failed to connect to MySQL Database")
  