import re
def capitalize_text(selection, text):
  array = ["FIO", "Surname", "Other"]
  if selection == array[0]: # FIO
    text = re.sub(r'\b\w', lambda m: m.group().upper(), text)
    text = re.sub(r'[^а-яА-Я\\s ]', '', text)  # удаляем все символы, кроме русских букв и пробелов
    return text
  elif selection == array[1]: # Surname
    text = re.sub(r'\b\w', lambda m: m.group().upper(), text)
    text = re.sub(r'[^а-яА-Я\\s-]', '', text)  # удаляем все символы, кроме русских букв и пробелов
    return text
  elif selection == array[2]:
    text = re.sub(r'\b\w', lambda m: m.group().upper(), text)
    text = re.sub(r'[^а-яА-Я\\s]', '', text)  # удаляем все символы, кроме русских букв и пробелов
    return text