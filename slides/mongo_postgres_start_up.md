# Установка СУБД

В этом уроке описано, как установить Postgres и MongoDB самомстоятельно. Такой подход **крайне не рекомендуется**, для установки этих дистрибутивов лучше пользоваться готовыми Docker-образами.
Однако, если с Докером не срослось - добро пожаловать!

## Установка Postgres

Теперь в Ubuntu нужно установить Postgres. Сначала добавим нужные репозитории
<pre>
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -;
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'
</pre>

Проведём установку с помощью стандартного менеджера пакетов apt-get
<pre>
sudo apt update
sudo apt-get install postgresql-10
</pre>

После установки рестартуем демона базы данных
<pre>
sudo systemctl stop postgresql.service
sudo systemctl start postgresql.service
sudo systemctl enable postgresql.service
sudo systemctl status postgresql.service
</pre>

Теперь нужно загрузить дамп в Postgres. Для этого перейдем в консоль Postgres
<pre>
sudo su -l postgres
</pre>

Мы переключимся в сеанс пользователя Postgres. Осталось загрузить текстовый дамп в Постгрю
<pre>
psql -d postgres -U postgres -1 -f $SOURCE_DATA/data/all_tables.dump
</pre>

Подключимся к БД и проверим, что данные загружены
<pre>
psql -U postgres -c "SELECT COUNT(*) FROM ratings;"
</pre>

Результат
<pre>
 count
--------
 777776
(1 row)
</pre>

Готово! Видео-туториал по установке и настройке среды [доступен по ссылке](https://www.youtube.com/watch?v=Qlfw-oH4QiI)

## Установка MongoDB

Выполним установку Mongo [по инструкции](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-18-04). Для установки воспользуемся пакетным менеджером
<pre>
sudo apt install -y mongodb
</pre>

После окончания установки проверим
<pre>
sudo systemctl status mongodb
</pre>
Результат работы команды
<pre>
● mongodb.service - An object/document-oriented database
   Loaded: loaded (/lib/systemd/system/mongodb.service; enabled; vendor preset: 
   Active: active (running) since Sat 2019-02-02 13:53:07 MSK; 3min 2s ago
     Docs: man:mongod(1)
 Main PID: 3853 (mongod)
    Tasks: 23 (limit: 4915)
   CGroup: /system.slice/mongodb.service
           └─3853 /usr/bin/mongod --unixSocketPrefix=/run/mongodb --config /etc/

~
</pre>

**Внимание**: чтобы вернуться в консоль, наберите
<pre>
q
</pre>

Подключимся к CLI MongoDB
<pre>
/usr/bin/mongo
</pre>

Результат
<pre>
VirtualBox:~$ /usr/bin/mongo
MongoDB shell version v3.6.3
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 3.6.3
</pre>

Чтобы выйти из консоли Mongo, наберите
<pre>
quit()
</pre>

Проверим, что доступны данные для загрузки
<pre>
ls $SOURCE_DATA/raw_data | grep test.json
</pre>

Выхлоп команды
<pre>
test.json
</pre>

Воспользуемся утилитой Mongoimport для загрузки данных
<pre>
/usr/bin/mongoimport --db pets --collection dogs --file $SOURCE_DATA/raw_data/test.json
</pre>

Результат работы команды
<pre>
2019-02-02T15:00:54.383+0300	connected to: localhost
2019-02-02T15:00:54.439+0300	imported 100 documents
</pre>

Проверим, что всё ок. Запустим Mongo
<pre>
mongo
</pre>

переключимся в созданную схему данных
<pre>
use pets;
</pre>

Результат
<pre>
switched to db pets
</pre>

Проверим, что json загрузился
<pre>
db.dogs.count()
</pre>

Результат
<pre>
100
</pre>

Всё готово! С MongoDB можно начинать работать.
