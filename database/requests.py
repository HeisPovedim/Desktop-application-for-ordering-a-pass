from database.connect import DB
from data.user import user

def addIndividualVisits(
    date_with, date_about, purpose,
    division, FIO,
    surname, name, patronymic, phone, email, organization, note, birthdate, passport_series, passport_number,
    document, photo,
    current_date,
  ):
  db = DB()
  cursor = db.cursor_dictionary
  
  username = user['username']
  query = f"SELECT id FROM users WHERE login='{username}'"
  cursor.execute(query)
  userId = cursor.fetchone()
  
  # information_for_the_pass
  sql = """
  INSERT INTO information_for_the_pass
  (
    validity_period_from,
    validity_period_for,
    purpose_of_the_visit
  ) VALUES (%s,%s,%s)"""
  val = (
    date_with,
    date_about,
    purpose
  )
  cursor.execute(sql,val)
  information_for_the_pass_id = cursor.lastrowid


  # receiving_party
  sql = "INSERT INTO receiving_party (division, FIO) VALUES (%s,%s)"
  val = (division, FIO)
  cursor.execute(sql,val)
  receiving_party_id = cursor.lastrowid
  
  
  # visitor_information
  sql = """
  INSERT INTO visitor_information
  (
    surname,
    name,
    patronymic,
    phone,
    email,
    organization,
    note,
    birthdate,
    passport_series,
    passport_number
  ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
  val = (
    surname,
    name,
    patronymic,
    phone,
    email,
    organization,
    note,
    birthdate,
    passport_series,
    passport_number
  )
  cursor.execute(sql, val)
  visitor_information_id = cursor.lastrowid
  
  
  # documents
  sql = """
  INSERT INTO documents_personal (pdf, photo) VALUES (%s,%s)"""
  val = (document,photo)
  cursor.execute(sql, val)
  documents_id = cursor.lastrowid
  
  print(information_for_the_pass_id, receiving_party_id, visitor_information_id, documents_id)
  
  sql = """
  INSERT INTO personal_visit
  (
    users_id,
    information_for_the_pass_id,
    receiving_party_id,
    visitor_information_id,
    documents_id,
    creation_time,
    status,
    reason
  ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
  val = (
    userId["id"],
    information_for_the_pass_id,
    receiving_party_id,
    visitor_information_id,
    documents_id,
    current_date,
    "checked",
    "no comment"
  )
  cursor.execute(sql, val)
  db.commit()


def addGroupVisits(
    date_with, date_about, purpose,
    division, FIO,
    surname, name, patronymic, phone, email, organization, note, birthdate, passport_series, passport_number,
    document, xlsx,
    current_date,
):
  db = DB()
  cursor = db.cursor_dictionary
  
  username = user['username']
  query = f"SELECT id FROM users WHERE login='{username}'"
  cursor.execute(query)
  userId = cursor.fetchone()
  
  # information_for_the_pass
  sql = """
  INSERT INTO information_for_the_pass
  (
    validity_period_from,
    validity_period_for,
    purpose_of_the_visit
  ) VALUES (%s,%s,%s)"""
  val = (
    date_with,
    date_about,
    purpose
  )
  cursor.execute(sql, val)
  information_for_the_pass_id = cursor.lastrowid
  
  # receiving_party
  sql = "INSERT INTO receiving_party (division, FIO) VALUES (%s,%s)"
  val = (division, FIO)
  cursor.execute(sql, val)
  receiving_party_id = cursor.lastrowid
  
  # visitor_information
  sql = """
  INSERT INTO visitor_information
  (
    surname,
    name,
    patronymic,
    phone,
    email,
    organization,
    note,
    birthdate,
    passport_series,
    passport_number
  ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
  val = (
    surname,
    name,
    patronymic,
    phone,
    email,
    organization,
    note,
    birthdate,
    passport_series,
    passport_number
  )
  cursor.execute(sql, val)
  visitor_information_id = cursor.lastrowid
  
  # documents
  sql = """
  INSERT INTO documents_group (pdf, list_visitors) VALUES (%s,%s)"""
  val = (document, xlsx)
  cursor.execute(sql, val)
  documents_id = cursor.lastrowid
  
  print(information_for_the_pass_id, receiving_party_id, visitor_information_id, documents_id)
  
  sql = """
  INSERT INTO group_visit
  (
    users_id,
    information_for_the_pass_id,
    receiving_party_id,
    visitor_information_id,
    documents_id,
    creation_time,
    status,
    reason
  ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
  val = (
    userId["id"],
    information_for_the_pass_id,
    receiving_party_id,
    visitor_information_id,
    documents_id,
    current_date,
    "checked",
    "no comment"
  )
  cursor.execute(sql, val)
  db.commit()
  
def getting_user_information():
  
  db = DB()
  cursor = db.cursor_dictionary
  
  username = user['username']
  
  cursor.execute(f"SELECT id, email, login FROM users WHERE login='{username}'")
  return cursor.fetchall()
