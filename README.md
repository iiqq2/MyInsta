# Этот проект является "Клоном инсты", отсюда и название MyIsta

## Инстркция по разворачиванию проекта:
- Скачайте проект, перейдите в основную папку и добавьте файл .env
> Для примира:\
>DEBUG = True или False\
>SECRET_KEY = Ваш Django_Sectet_Key\
>Name = Ваш Db_name\
>User = Ваш Db_user\
>Password = Ваш Db_password\
>Host = Ваш Db_localhost\
>Port = Ваш Db_Port\
>SOCIAL_AUTH_VK_OAUTH2_KEY = Ваш key от вк аунтификации\
>SOCIAL_AUTH_VK_OAUTH2_SECRET = Ваш secret от вк аунтификации\
- После "py manage.py migrate" и "py manage.py runserver"