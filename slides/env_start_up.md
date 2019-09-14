# Подготовка машины к работе

# Урок 1. Базовая настройка рабочей среды

Занятия будут проходить в ОС Ubuntu 18.04 LTS. Установка необходимых баз данных (Mongo, Postgres, Redis, etc.)
осуществляется с помощью утилиты виртуализации Docker, либо  прямо в систему Ubuntu. Доступны оба варианта, но докер более предпочтителен.

**Примечание:** Если у Вас MacOS - сойдёт, она похожа на Ubuntu и утилиты командной строки там примерно такие же, курс можно будет пройти.
Если у Вас Windows, то будет сложнее, но в целом тоже не критично - главное, чтобы было куда установить Postgres (обязательно!) и остальные дистрибутивы (Mongo, Redis), опционально. 

## Установка и настройка операционной системы Ubuntu

Ввесь курс можно проходить и без Ubuntu, но с трудностями винды или мака придётся разбираться при помощи коллег и интернетов, спикер курса не поможет.
Если ОС Ubuntu не является основной операционной системой, то можно установить её следующими способами 

* С помощью VirtualBox [по этой инструкции](http://profitraders.com/Ubuntu/VirtualBoxUbuntuInstall.html)
* с помощью ПО VMWare [по этой инструкции](https://www.quora.com/How-do-I-install-Ubuntu-using-VMware-on-Windows-10) или VirtualBox
* с помощью облачного сервиса Google Cloud [по этой инструкции](#ubuntu-google-cloud) или любого другого, например Яндекс.Облако.

После того, как убунта установлена (любым способом), нужно обновить список пакетов. Для этого запустим в консоли команду:

<pre>
sudo apt-get update && sudo apt-get -y upgrade;
</pre>

Эта команда обновит пакетный менеджер apt-get. После этого установить менеджер пакетов pip и вспомогательные утилиты (unzip, git):

<pre>
sudo apt-get install python-pip unzip git;
</pre>

Пакет pip - это менеджер пакетов python, его помощью можно будет устанавливать python библиотеки. Утилита unzip - программа для распаковки архивов.

С помощью pip установим библиотеки **requests** и **tqdm**, они нужны чтобы в дальнейшем более удобно загрузить файлы с Google Drive:
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
export SOURCE_DATA="/usr/local/share/source_data"
</pre>

После этого закроем файл с помощью комбинации **ctrl + O**, нажать Enter, затем **ctrl + X**, подтвердить **Y**, затем **ctrl + X** и выполним в терминале команду source, чтобы применить изменения:
<pre>
source ~/.bashrc
</pre>

Эти действия мы совершили для того, чтобы более удобно настроить рабочую среду: скачать данные, залить их в Postgres и т.д.
Мы установили переменную среды **SOURCE_DATA** - туда, в эту директорию, будет распакован архив с данными, которые будем загружать в Postgres - это набор `csv` файлов.
Чтобы проверить, как применились изменения выполним в консоли команду **echo $SOURCE_DATA** - должны увидеть в результат **/usr/local/share/source_data**.

**Справка** команда *echo* "печатает" значение переменной среды *$SOURCE_DATA*, где значок *$* является служебным.

Следующим шагом директорию нужно создать и дать самые широкие права на доступ туда. Начнём с того, что оздадим директорию:
<pre>
sudo mkdir $SOURCE_DATA;
</pre>

**Справка** для работы в консоли будем использовать базовые команды Linux

* Команда *sudo* позволяет запустить другие команды с правами Администратора системы
* Команда *mkdir* создаёт пустую директорию
* Команда *ls* печатает список файлов, которые находятся в директории.
* Команда *chmod 777* разрешает cоздание и удаление файлов из директории *$SOURCE_DATA* всем пользователям без исключения
* Команда *cd* позволяет сменить директорию.

Установим самые широкие права на чтение и запись в директорию
<pre>
sudo chmod 777 $SOURCE_DATA;
</pre>


Перейдём в директорию *$SOURCE_DATA* и создадим вспомогательные директории:
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

Теперь скачаем текстовые данные в формате csv, которые могут пригодиться для загрузки в Postgres в следующих частях курса. Запускаем скачивание файла - zip архива с данными. Архив весит примерно 23Mb
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


## Работа с Docker

Для установки системы виртуализации Docker на официальном сайте есть прекрасные пошаговые инструкции для всех основных ОС

* [тут Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [тут MacOS](https://docs.docker.com/docker-for-mac/install/)
* [тут Windows](https://docs.docker.com/docker-for-windows/install/)

Если у Windows, то для установки нужно использовать вот эту инструкцию:  https://docs.docker.com/toolbox/toolbox_install_windows/ 

Установим docker, согласно [инструкции для Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/).
Проверьте, что всё работает с помощью запуска команды
<pre>
docker run hello-world
</pre>

Если увидите ответное приветствие от Docker - готово, вы великолепны! Если не работает без  sudo - продолжайте настройку по инструкции.
Кроме докера поставим docker-compose

<pre>
sudo apt-get install docker-compose
</pre>

Подготовка завершена! Один раз проделав этот пункт, можно к нему больше не возвращаться

# Урок 2. Запуск среды для хранения данных в контейнере

В этом уроке поговорим о том, как научится использовать Postgres в Docker контейнере

## Базовое использование Docker образов

Теперь, когда Docker установлен, для дальнейшей работы нужно сделать несколько важных действий

* создать сеть `aviation_network`, по которой контейнеры буду передавать данные
* поднять контейнер `aviation-postgres` с Postgres-сервером, подключить его к сети `aviation_network`
* поднять контейнер с клиентом `psql` для доступа к Postgres
* перелить данные из csv-файлов в таблицы Postgres с помощью `psql` клиента

Чтобы выполнить эти действия, [следуйте данной инструкции](./docker_start_up.md)

## Автоматизируем работу с Docker

Переходим в директорию с докер-файлами
<pre>
cd data_management/docker_compose/data_client
</pre>

Мы научились использовать готовые докер-образы, давайте попробуем создать свой собственный! Чтобы создать образ, его нужно [описать в виде Dockerfile](../docker_compose/data_client/Dockerfile)

Запускаем сборку контейнера. В консоли побежит информация о сборке контейнера - поцесс может занять несколько минут и требует хорошего интернет-канала:
<pre>
docker build -t aviation_data_client:latest .
</pre>

Когда контейнер собран, подключимся в термина контейнера с помощью команды
<pre>
docker run --volume "${SOURCE_DATA}/raw_data":"/usr/share/raw_data" --network aviation_network -it --rm aviation_data_client:latest bash
</pre>

Проверим, что директория с данными успешно подключилась:
<pre>
ls "/usr/share/raw_data"
</pre>

Ответ
<pre>
credits.csv          links.csv            movies_metadata.csv  ratings_small.csv
keywords.csv         links_small.csv      ratings.csv
</pre>

Как видно csv-файлы присутствуют, контейнер запущен! Можно начинать работу. Чтобы прервать работу терминала, выполните команду `exit`.

Docker-контейнер можно рассматривать как программу, которуу запускаем командой `docker run`.
Для удобства разработки таких вот "программ" используется [специальный файл docker-entrypoint.sh](../docker_compose/data_client/docker-entrypoint.sh)
Команды из этого файла начинают исполняться, когда вы запускаете контейнер с помощью `docker run`.

В прошлом уроке мы научились загружать данные в Postgres. Давайте автоматизируем этот процесс, который состоит из двух этапов:
* создание таблиц
* импорт данных из csv файлов

Рассмотрим [скрипт для загрузки данных load_data.sh](../docker_compose/data_client/app/load_data.sh). Этот скрипт запускается с помощью `docker-entrypint.sh` следующим образом:

<pre>
docker run -v "$(pwd)/app":"/www/app" -v "${SOURCE_DATA}/raw_data":"/usr/share/raw_data" -e APP_POSTGRES_HOST=aviation-postgres  --network aviation_network -it --rm aviation_data_client:latest load
</pre>

После того, как все данные загружены в Postgres - проверим подключение к БД и наличие данных
<pre>
docker run --network aviation_network -it --rm aviation_data_client:latest psql -h aviation-postgres -U postgres -c "SELECT COUNT(*) as num_ratings FROM ratings"
</pre>

Чтобы подключиться в интерактивный терминал для работы с Postgres достаточно набрать
<pre>
docker run --network aviation_network -it --rm aviation_data_client:latest psql -h aviation-postgres -U postgres
</pre>

Готово! Мы создали кастомный контейнер для работы с данными, описав его с помощью Dockerfile

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
