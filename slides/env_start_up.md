# Подготовка машины к работе

## Описание рабочей среды

Занятия будут проходить в ОС Ubuntu 18.04 LTS. Установка необходимых баз данных (Mongo, Postgres, Redis, etc.)
осуществляется прямо в систему Ubuntu, либо  с помощью утилиты виртуализации Docker. Доступны оба варианта, но докер - только для опытных пользователей.

**Примечание:** Если у Вас MacOS - сойдёт, она похожа на Ubuntu и утилиты командной строки там примерно такие же, курс можно будет пройти.
Если у Вас Windows, то будет сложнее, но в целом тоже не критично - главное, чтобы было куда установить Postgres (обязательно!) и остальные дистрибутивы, опционально. 

## Установка и настройка операционной системы Ubuntu

Ввесь курс будет проходить на базе дистрибутива Ubuntu - можно и без убунты, но с трудностями винды или мака придётся разбираться при помощи коллег и интернетов, спикер курса не поможет.
Если ОС Ubuntu не является основной операционной системой, то можно установить её следующими способами 

* с помощью ПО VMWare [по этой инструкции](https://www.quora.com/How-do-I-install-Ubuntu-using-VMware-on-Windows-10) или VirtualBox
* с помощью облачного сервиса Google Cloud [по этой инструкции](#ubuntu-google-cloud)


После того, как убунта установлена (любым способом), нужно обновить список пакетов. Для этого запустим в консоли команду:

<pre>
sudo apt-get update && sudo apt-get -y upgrade
</pre>

Эта команда обновит пакетный менеджер apt-get. После этого установить менеджер пакетов pip и вспомогательные утилиты (unzip, git):

<pre>
sudo apt-get install python-pip unzip git
</pre>

Пакет pip - это менеджер пакетов python, его помощью можно будет устанавливать python библиотеки. Утилита unzip - программа для распаковки архивов.

С помощью pip установим библиотеки **requests** и **tqdm**:
<pre>
pip install requests;
pip install tqdm;
</pre>

Далее нужно отредактировать файл ~/.bashrc и установить там переменные среды. Для этого откроем файл с помощью редактора nano:
<pre>
nano ~/.bashrc
</pre>

Нажимаем комбинацию **ctrl + V**, чтобы долистать до конца файла, затем копируем переменные и их значения и вставляем в открытый файл с помощью комбинации **ctrl + shift + V**
<pre>
export APP_MONGO_HOST=localhost
export APP_MONGO_PORT=27017
export APP_POSTGRES_HOST=localhost
export APP_POSTGRES_PORT=5432
export APP_REDIS_HOST=localhost
export APP_REDIS_PORT=6379
export SOURCE_DATA="/usr/local/share/source_data"
</pre>

После этого закроем файл с помощью комбинации **ctrl + O**, нажать Enter, затем **ctrl + X**, подтвердить **Y**, затем **ctrl + X** и выполним в терминале команду source, чтобы применить изменения:
<pre>
source ~/.bashrc
</pre>

Эти действия мы совершили для того, чтобы более удобно настроить рабочую среду: скачать данные, залить их в Postgres b n/l/
Мы установили переменную среды **SOURCE_DATA** - туда, в эту директорию, будет распакован архив с данными, которые будем загружать в Postgres.
Следующим шагом директорию нужно создать и дать самые широкие права на доступ туда
Чтобы проверить, как применились изменения выполним в консоли команду **echo $SOURCE_DATA** - должны увидеть в результат **/usr/local/share/source_data**.

**Справка** команда *echo* "печатает" значение переменной среды *$SOURCE_DATA*, где значок *$* является служебным.

Создадим директорию
<pre>
sudo mkdir $SOURCE_DATA;
</pre>

**Справка** для работы в консоли будем использовать базовые команды Linux

* Команда *sudo* позволяет запустить другие команды с правами Администратора системы
* Команда *mkdir* создаёт пустую директорию
* Команда *ls* печатает список файлов, которые находятся в директории.
* Команда *chmod 777* разрешает cоздание и удаление файлов из директории *$SOURCE_DATA* всем пользователям без исключения
* Команда *cd* позволяет сменить директорию.

и дадим нужные права
<pre>
sudo chmod 777 $SOURCE_DATA;
</pre>


Перейдём в созданную директорию и создадим вспомогательные директории:
<pre>
cd $SOURCE_DATA;

mkdir $SOURCE_DATA/raw_data; mkdir $SOURCE_DATA/pg_data; mkdir $SOURCE_DATA/data;
</pre>

Проверим, что все директории созданы успешно

<pre>
ls $SOURCE_DATA
</pre>

Результат работы команды
<pre>
raw_data, pg_data, data
</pre>

## Загрузка дампа БД  и csv данных

Теперь данные, которые я заранее залил на Google Drive нужно перенести на локальную машину. Для этого  склонируем полезный репозиторий (содержит утилиту для скачивания с Google Cloud).

Мы используем данные [The Movies Dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset) c Kaggle.

<pre>
rm -rf download_google_drive; git clone https://github.com/chentinghao/download_google_drive.git
</pre>

Загружаем дамп БД, чтобы создать нужные для работы таблицы
<pre>
python download_google_drive/download_gdrive.py 1uWZjmm9vwxZMplMqUtn0r-M16a0ochQa $SOURCE_DATA/data/all_tables.dump
</pre>

Теперь скачаем текстовые данные в формате csv, которые могут пригодиться для загрузки в Python в следующих частях курса. Запускаем скачивание файла - zip архива с данными. Архив весит примерно 23Mb
<pre>
python download_google_drive/download_gdrive.py 1D3CcWOSw-MUx6YvJ_4dqOLHZAh-6uTxK data.zip
</pre>

Сначала распаковываем архив с данными.
<pre>
unzip data.zip -d "$SOURCE_DATA"/raw_data;
</pre>

Мы увидим процесс извлечения данных - это csv и json файлы

<pre>
Archive:  data.zip
  inflating: /tmp/data/ratings.csv
  inflating: /tmp/data/ratings_small.csv
  inflating: /tmp/data/links.csv
  inflating: /tmp/data/links_small.csv
  inflating: /tmp/data/keywords.csv
  inflating: /tmp/data/movies_metadata.csv
  inflating: /tmp/data/credits.csv
</pre>

Теперь скачиваем репозиторий курса - там хранятся материалы для домашних работ.

<pre>
git clone https://github.com/adzhumurat/data_management.git
</pre>


### Установка Postgres

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

## Установка Mongo

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

## Установка docker

Установим docker, согласно [Инструкции тут](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

Кроме докера поставим docker-compose

<pre>
sudo apt-get install docker-compose
</pre>

Подготовка завершена! Один раз проделав этот пункт, можно к нему больше не возвращаться

### Работа c репозиторием в Docker

Переходим в директорию с докер-файлами
<pre>
cd data_management/docker_compose
</pre>

Запускаем сборку контейнера. В консоли побежит информация о сборке контейнера. После окончания сборки мы автоматически подключимся к командной строке Debian, т.е. внутрь контейнера:
<pre>
make client
</pre>

Проверим, что директория с данными успешно подключилась:
<pre>
/ # ls /data
credits.csv          links.csv            movies_metadata.csv  ratings_small.csv
keywords.csv         links_small.csv      ratings.csv
</pre>

Как видно csv-файлы присутствуют, контейнер запущен! можно начинать работу.


Запускаем скрипт для загрузки файлов в Postgres
<pre>
bash /home/load_data.sh
</pre>

После того, как всё данные загружены в Postgres - проверим подключение к БД:

Подключение к Postgres
<pre>
psql --host $APP_POSTGRES_HOST -U postgres -c "SELECT COUNT(*) as num_ratings FROM ratings"
</pre>

## Решение проблем с docker

Если контейнер не стартует с ошибкой
<pre>
docker: Error response from daemon: Conflict. The container name "/some-postgres" is already in use by container "2a99cb6629b78e7b5b6747a9bd453263940127909d91c8517e9ee0b230e60768". You have to remove (or rename) that container to be able to reuse that name.
</pre>

То контейнер уже создан и можно стартовать его
<pre>
sudo docker start 2a99cb6629b78e7b5b6747a9bd453263940127909d91c8517e9ee0b230e60768
</pre>

Если не помогло - надо бы остановить все запущенные докер-образы и удалить их

<pre>
sudo docker stop $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)
</pre>

Удаление всех образов
<pre>
docker rmi $(docker images -q)
</pre>

Параметры docker run, остальные параметры [тут](https://docs.docker.com/v1.11/engine/reference/commandline/run/)

<code>
--name - Assign a name to the container

-d, --detach - Run container in background and print container ID

-e - устанавливаем переменную среды

-it - запустить интеракцивный терминал
</pre>

# Ubuntu Google Cloud

Как установить - по инструкции отсюда: https://cloud.google.com/compute/docs/quickstart-linux

Внимание! В инструкции установка Debian, а нам нужна Ubuntu 18.04. Эта опция выбирается в меню Boot Disk

![выбор ОС](https://habrastorage.org/webt/vl/dt/3m/vldt3mgct8jq3n6n9oa3pmyug_a.png "boot disk")

После установики ваш инстанс можно будет найти на этой странице https://console.cloud.google.com/compute/instances

![страница с инстансами](https://habrastorage.org/webt/cb/fx/qz/cbfxqzxqcdo0atxs9eg_c-t3jby.png "Google cloud instances")
