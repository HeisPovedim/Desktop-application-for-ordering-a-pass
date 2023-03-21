from database.connect import DB
from data.user import user

# ДОБАВЛЕНИЕ ИНДИВИДУАЛЬНОЙ ЗАЯВКИ В БД
def addPersonalVisit(
    date_with, date_about, purpose,
    division, FIO,
    surname, name, patronymic, phone, email, organization, note, birthdate, passport_series, passport_number,
    document, photo,
    current_date,
  ):
  db = DB()
  cursor = db.cursor_dictionary
  
  cursor.execute(f"SELECT id FROM users WHERE login='{user['username']}'")
  userId = cursor.fetchone()
  
  # pass_information
  sql = """
  INSERT INTO pass_information
  (
    date_from,
    date_by,
    visit_purpose
  ) VALUES (%s,%s,%s)"""
  val = (
    date_with,
    date_about,
    purpose
  )
  cursor.execute(sql,val)
  pass_information_id = cursor.lastrowid


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
  INSERT INTO documents_personal (document, photo) VALUES (%s,%s)"""
  val = (document,photo)
  cursor.execute(sql, val)
  documents_id = cursor.lastrowid
  
  sql = """
  INSERT INTO personal_visit
  (
    users_id,
    pass_information_id,
    receiving_party_id,
    visitor_information_id,
    documents_id,
    creation_time,
    status
  ) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
  val = (
    userId["id"],
    pass_information_id,
    receiving_party_id,
    visitor_information_id,
    documents_id,
    current_date,
    "checked"
  )
  cursor.execute(sql, val)
  db.commit()

# ДОБАВЛЕНИЕ ГРУППОВОЙЙ ЗАЯВКИ В БД
def addGroupVisits(
    date_with, date_about, purpose,
    division, FIO,
    surname, name, patronymic, phone, email, organization, note, birthdate, passport_series, passport_number,
    document, xlsx,
    current_date,
):
  db = DB()
  cursor = db.cursor_dictionary
  
  cursor.execute(f"SELECT id FROM users WHERE login='{user['username']}'")
  userId = cursor.fetchone()
  
  # pass_information
  sql = """
  INSERT INTO pass_information
  (
    date_from,
    date_by,
    visit_purpose
  ) VALUES (%s,%s,%s)"""
  val = (
    date_with,
    date_about,
    purpose
  )
  cursor.execute(sql, val)
  pass_information_id = cursor.lastrowid
  
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
  sql = "INSERT INTO documents_group (document, visitor_list) VALUES (%s,%s)"
  val = (document, xlsx)
  cursor.execute(sql, val)
  documents_id = cursor.lastrowid
  
  sql = """
  INSERT INTO group_visit
  (
    users_id,
    pass_information_id,
    receiving_party_id,
    visitor_information_id,
    documents_id,
    creation_time,
    status
  ) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
  val = (
    userId["id"],
    pass_information_id,
    receiving_party_id,
    visitor_information_id,
    documents_id,
    current_date,
    "checked"
  )
  cursor.execute(sql, val)
  db.commit()
  
# ПОЛУЧЕНИЕ ИНФОРМАЦИИ О ПОЛЬЗОВАТЕЛЕ
def getting_user_information():
  db = DB()
  cursor = db.cursor_dictionary
  
  cursor.execute(f"SELECT id, email, login FROM users WHERE login='{user['username']}'")
  return cursor.fetchone()

# ПОЛУЧЕНИЕ ПЕРСОНАЛЬНЫХ ЗАЯВОК
def getting_personal_applications():
  db = DB()
  cursor = db.cursor_dictionary

  cursor.execute(f"SELECT id FROM users WHERE login='{user['username']}'")
  userId = cursor.fetchone()
  
  sql = f"""
  SELECT
    p.receiving_party_id,
    p.creation_time,
    p.status,
    r.division
  FROM
    personal_visit p
  LEFT JOIN
    receiving_party r ON r.id = p.receiving_party_id
  WHERE
    p.users_id = {userId['id']}
  """
  
  cursor.execute(sql)
  return cursor.fetchall()

# ПОЛУЧЕНИЕ ГРУППОВЫХ ЗАЯВОК
def getting_group_applications():
  db = DB()
  cursor = db.cursor_dictionary
  
  cursor.execute(f"SELECT id FROM users WHERE login='{user['username']}'")
  userId = cursor.fetchone()
  
  sql = f"""
  SELECT
    p.receiving_party_id,
    p.creation_time,
    p.status,
    r.division
  FROM
    group_visit p
  LEFT JOIN
    receiving_party r ON r.id = p.receiving_party_id
  WHERE
    p.users_id = {userId['id']}
  """
  
  cursor.execute(sql)
  return cursor.fetchall()
  
    
    
  