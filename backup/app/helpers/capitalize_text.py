import re
def capitalize_text(text):
  text = re.sub(r'\b\w', lambda m: m.group().upper(), text)
  text = re.sub(r'[^а-яА-Я\\s ]', '', text)  # удаляем все символы, кроме русских букв и пробелов
  return text