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

    # курсор для выполнения запросов
    self.cursor = self.connect.cursor()
    
    if self.connect.is_connected():
      print("Connected to MySQL Database")
    else:
      print("Failed to connect to MySQL Database")

  def commit(self):
    self.connect.commit()

  def close(self):
    self.cursor.close()
    self.connect.close()