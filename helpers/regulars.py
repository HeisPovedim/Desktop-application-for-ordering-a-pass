import re
def re_login(text):
  return re.sub(r'[^a-zA-Z]+$', '', text.title())

def re_password(text):
  return re.sub(r'[^a-zA-Z0-9\-]+$', '', text)