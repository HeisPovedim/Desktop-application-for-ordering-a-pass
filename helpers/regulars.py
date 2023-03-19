import re
def re_login(text):
  return re.sub(r'[^a-zA-Z]+$', '', text.title())

def re_password(text):
  return re.sub(r'[^a-zA-Z0-9\-]+$', '', text)

def re_email(text):
  return re.sub(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', '', text)