# fBlog

##Установка виртуального окружения:
####из корневой директории
```sh
virtualenv -p python3 ./venv
```
##Активация виртуального окружения:
####из корневой директории
```sh
source venv/bin/activate
```
##Установка Flask:
```sh
pip install flask
```

#####Запись зависимостей в файл:
######из директории blog
```sh
pip freeze > requirements.txt
```