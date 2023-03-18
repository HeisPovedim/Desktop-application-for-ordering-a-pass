# Настольное приложение для заказа пропуска
___
## Информация о проекте
Используемые библиотеки:
- PyQt6
- dnspython
- mysql-connector-python

Проект следует запускать через файл - `executable.py`
```
Web-service-for-ordering-a-pass
├─ data
├─ files
├─ helpers
├─ img
├─ interface
├─ MySQL
└─ executable.py ←-THIS
```
Для запуска проекта необходимо находится в коневой папке **Web-service-for-ordering-a-pass**.</br>
После мы открываем командную строку в нашей папке или с помощью команды **cd** переходим к нашему проекту (пример: `cd D:\Project\GitHub\Web-service-for-ordering-a-pass`) и запускаем скрипт путем ввода в консоль команды: `python.exe executable.py`

## Настройка БД для проекта
В проекте присутствует **SQL Script** для быстрого развертывания БД, для этого понадобится программа [**MySQL Workbench**](https://www.mysql.com/products/workbench/), сам скрипт лежит в директории **MySQL**:
```
Web-service-for-ordering-a-pass
├─ data
├─ files
├─ helpers
├─ img
├─ interface
├─ MySQL
│  ├─ config.py
│  ├─ connect_db.py
│  ├─ Models.mwb
│  ├─ Models.mwb.bak
│  ├─ SQL_Script ←-THIS
│  └─ SQL.sql
├─ __init__.py
└─ executable.py
```