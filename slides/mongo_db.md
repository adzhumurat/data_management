# Mongo command line interface

Подключение к Mongo-серверу осуществляется с помощью утилиты Mongo (в докер-контейнере она уже установлена)

```shell
python3 upstart.py -s mongo
```

Результат

```shell
MongoDB shell version v4.0.0
connecting to: mongodb://mongo_host:27017/
MongoDB server version: 4.0.0
Welcome to the MongoDB shell.
For interactive help, type "help".
---

>
```

В консоли существует множество команд


stats - статистика MongoDB

```python
db.stats()
```

Результат

```json
{
	"db" : "test",
	"collections" : 0,
	"views" : 0,
	"objects" : 0,
	"avgObjSize" : 0,
	"dataSize" : 0,
	"storageSize" : 0,
	"numExtents" : 0,
	"indexes" : 0,
	"indexSize" : 0,
	"fileSize" : 0,
	"fsUsedSize" : 0,
	"fsTotalSize" : 0,
	"ok" : 1
}
```

Переключимся в схему данных `test_db`

```sql
use test_db
```

Результат

```python
switched to db test_db
```

Добавим в коллекцию документов `test_collection` один документ

```python
db.test_collection.insert({name: 'Pepe', gender: 'm', weight: 40})
```

Результат

```python
WriteResult({ "nInserted" : 1 })
```

Снова посмотрим статистику по БД - мы увидим одну созданную коллекцию:
```python
db.stats()
```

Результат

```json
{
	"db" : "test_db",
	"collections" : 1,
	"views" : 0,
	"objects" : 1,
	"avgObjSize" : 67,
	"dataSize" : 67,
	"storageSize" : 4096,
	"numExtents" : 0,
	"indexes" : 1,
	"indexSize" : 4096,
	"fsUsedSize" : 42377572352,
	"fsTotalSize" : 244529655808,
	"ok" : 1
}
```

Как видно, у нас в БД появилась новая коллекция и один объект. В любой момент мы можем проверить, какие объекты хранятся в БД:

```python
db.getCollectionNames()
```

Результат

```json
[ "test_collection" ]
```

Для фильтрации записей используем find (аналог WHERE из SQL)

```python
db.test_collection.find({'name': 'Pepe'})
```

Результат

```json
{ "_id" : ObjectId("5b56a66a64669cd544d5fd73"), "name" : "Pepe", "gender" : "m", "weight" : 40 }
```

JSON, который передaётся в функцию find называется "селектор".
Селектор формирует набор документов из коллекции, которые отвечают уcловиям, перечисленным в селекторе.

Добавим новый документ в коллекцию с отличающимся набором полей:

```python
db.test_collection.insert({name: 'Lolo', gender: 'f', home: 'Moscow', student: false})
```

Результат

```python
WriteResult({ "nInserted" : 1 })
```

Воспользуемся командой `find()`, которая является аналогом для SELECT в стандарте SQL.
```python
db.test_collection.find()
```

Результат

```json
{ "_id" : ObjectId("5b56a66a64669cd544d5fd73"), "name" : "Pepe", "gender" : "m", "weight" : 40 }
{ "_id" : ObjectId("5b56b32e64669cd544d5fd74"), "name" : "Lolo", "gender" : "f", "home" : "Moscow", "student" : false }
```

Мы добавили в нашу коллекцию новый документ с другим набором полей. Такое добавление было бы невозможно в реляционной БД, где набор полей фиксируется в момент создания таблицы.

Для удаления записей используется функция `.remove()`, в которую нужно передать селектор

```json
db.test_collection.remove({home: "Moscow"})
```

Результат

```python
WriteResult({ "nRemoved" : 1 })
```

Проверим, какие элементы остались в коллекции

```python
db.test_collection.find()
```


Результат

```json
{ "_id" : ObjectId("5b56a66a64669cd544d5fd73"), "name" : "Pepe", "gender" : "m", "weight" : 40 }
```

В селекторы можно передавать специальные операторы, которые эквивалентны условиям в WHERE запросов SQL:

```json
db.test_collection.find({gender: 'm', weight: {$gt: 700}})
```

Тут ничего не нашли - это ожидаемо. Поправим условие в селекторе:

```json
db.test_collection.find({gender: 'm', weight: {$lt: 700}})
```

Результат

```json
{ "_id" : ObjectId("5b56a66a64669cd544d5fd73"), "name" : "Pepe", "gender" : "m", "weight" : 40 }
```

Так, например, оператор $exists проверяет наличие у объекта того или иного поля. Внутри селектора условия можно объединять с помощью оператора $or
```json
db.test_collection.find({$or: [{gender: 'm'}, {home: 'Moscow'}]})
```

Результат

```json
{ "_id" : ObjectId("5b56a66a64669cd544d5fd73"), "name" : "Pepe", "gender" : "m", "weight" : 40 }
{ "_id" : ObjectId("5b56b78664669cd544d5fd75"), "name" : "Lolo", "gender" : "f", "home" : "Moscow", "student" : false }
```

## Обновление записей

Обновление производится функцией update, попробуем её применить

```json
db.test_collection.update({home: 'Moscow'},{student: true})
```

Результат

```json
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
```

Проверим, что новый документ появился в коллекции
```json
db.test_collection.find({home: 'Moscow'})
```

Ничего не нашли, что случилось? Выведем все документы коллекции
```json
db.test_collection.find()
```

Результат

```json
{ "_id" : ObjectId("5b56a66a64669cd544d5fd73"), "name" : "Pepe", "gender" : "m", "weight" : 40 }
{ "_id" : ObjectId("5b56b78664669cd544d5fd75"), "student" : true }
```

Функция update не просто изменила это поля, а переписала весь документ. Чтобы такого не произошло, нужно использовать модификатор $set

Вернём нашу запись на место
```json
db.test_collection.insert({name: 'Lolo', gender: 'f', home: 'Moscow', student: false})
```

Результат

```json
WriteResult({ "nInserted" : 1 })
```

Проведём правильный update
```json
db.test_collection.update({home: 'Moscow'}, {$set: {student: true}})
```

Результат

```json
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
```


Проверим, что всё успешно
```json
db.test_collection.find()
```

Результат

```json
{ "_id" : ObjectId("5b571bf081d67789509607f1"), "name" : "Lolo", "gender" : "f", "home" : "Moscow", "student" : true }
```


Третий параметр в методе update позволяет создать запись, если она отсутствует - т.н. upsert (UPDATE + INSERT)

Попробуем выполнить update записи, которой нет
```json
db.test_collection.update({home: 'Perm'}, {$set: {student: false}})
```

Результат

```json
WriteResult({ "nMatched" : 0, "nUpserted" : 0, "nModified" : 0 })
```

Как изменилась коллекция? Никак =[
```json
db.test_collection.find()
```

Результат

```json
{ "_id" : ObjectId("5b571bf081d67789509607f1"), "name" : "Lolo", "gender" : "f", "home" : "Moscow", "student" : true }
```

Попробуем функционал UPSERT:
```json
db.test_collection.update({home: 'Perm'}, {$set: {student: false}}, true)
```

Результат

```json
WriteResult({
	"nMatched" : 0,
	"nUpserted" : 1,
	"nModified" : 0,
	"_id" : ObjectId("5b57207bbff183a0a45dcfb3")
})
```

Проверим, как изменилась коллекция
```json
db.test_collection.find()
```

Результат

```json
{ "_id" : ObjectId("5b571bf081d67789509607f1"), "name" : "Lolo", "gender" : "f", "home" : "Moscow", "student" : true }
{ "_id" : ObjectId("5b57207bbff183a0a45dcfb3"), "home" : "Perm", "student" : false }
```

По умолчанию будет обновлён один из документов, попадающих под условия селектора. Четвёртый параметр команды позволяет осуществлять массовую вставку (обновление) документов.

Есть другие модификаторы, например $inc (увеличивает скаляр) или $push (добавляет в массив) - о них можно почитать
в документации по [Mongo](https://docs.mongodb.com/manual/reference/operator/update/)

# Mongo - продвинутые техники

Отсутствуют джойны. Чтобы как-то моделировать джойны предлагается особенным образом формировать документы - чтобы сохранять связи между различными коллекциями

```json
db.posts.insert({day: 'Wed', author: ObjectId("5b571bf081d67789509607f1")})
db.posts.insert({day: 'Sat', author: ObjectId("5b571bf081d67789509607f1")})
db.posts.insert({day: 'Sat', author: ObjectId("5b57207bbff183a0a45dcfb3")})
```

Проверим, что записалось в БД
```json
db.posts.find()
```

Результат

```json
{ "_id" : ObjectId("5b57392b81d67789509607f2"), "day" : "Wed", "author" : ObjectId("5b571bf081d67789509607f1") }
{ "_id" : ObjectId("5b57393481d67789509607f3"), "day" : "Sat", "author" : ObjectId("5b571bf081d67789509607f1") }
{ "_id" : ObjectId("5b57394381d67789509607f4"), "day" : "Sat", "author" : ObjectId("5b57207bbff183a0a45dcfb3") }
```

Вместо джойна используем find по полю ObjectId

```json
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")})
```

Результат

```json
{ "_id" : ObjectId("5b57392b81d67789509607f2"), "day" : "Wed", "author" : ObjectId("5b571bf081d67789509607f1") }
{ "_id" : ObjectId("5b57393481d67789509607f3"), "day" : "Sat", "author" : ObjectId("5b571bf081d67789509607f1") }
```

Пo умолчанию возвращаются все поля документа. Это поведение можно изменить:
```json
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")}, {day: 1})
```

Результат

```json
{ "_id" : ObjectId("5b57392b81d67789509607f2"), "day" : "Wed" }
{ "_id" : ObjectId("5b57393481d67789509607f3"), "day" : "Sat" }
```

Служебное поле _id возвращается всегда - его можно выключить в явном виде

```json
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")}, {day: 1, _id: 0})
```

Результат

```json
{ "day" : "Wed" }
{ "day" : "Sat" }
```

В остальных случаях включение и исключение полей нельзя смешивать.

Порядок выдачи изменяется командой .sort():

```json
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")}, {day: 1, _id: 0}).sort({day: 1})
```

Результат

```json
{ "day" : "Sat" }
{ "day" : "Wed" }
```

или в обратном порядке

```json
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")}, {day: 1, _id: 0}).sort({day: -1})
```

Результат

```json
{ "day" : "Wed" }
{ "day" : "Sat" }
```

Так же можно управлять количеством записей в выдаче и смещением от начала списка

Полная выдача:
```json
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")}, {day: 1, _id: 0}).sort({day: -1})
```

Результат

```json
{ "day" : "Wed" }
{ "day" : "Sat" }
```

Задаём смещение
```json
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")}, {day: 1, _id: 0}).sort({day: -1}).limit(2).skip(1)
```

Результат

```json
{ "day" : "Sat" }
```

Гибкость курсора позволяет управлять нагрузкой на Mongo, так как курсор умеет делать смещения без непосредственного чтения записей

## Загрузка JSON

Для загрузки JSON выполним скрипт формирования JSON - это будут случайные картинки собачек, получаемых по API

```json
rm -f test.json; for i in $(seq 100 $END); do curl "https://dog.ceo/api/breeds/image/random">>test.json; done;
```

На выходе получаем JSON-файл
```json
head test.json;
```

Результат

```json
{"status":"success","message":"https:\/\/images.dog.ceo\/breeds\/weimaraner\/n02092339_1013.jpg"},
{"status":"success","message":"https:\/\/images.dog.ceo\/breeds\/basenji\/n02110806_5971.jpg"},
{"status":"success","message":"https:\/\/images.dog.ceo\/breeds\/dingo\/n02115641_5815.jpg"},
{"status":"success","message":"https:\/\/images.dog.ceo\/breeds\/corgi-cardigan\/n02113186_10475.jpg"},
{"status":"success","message":"https:\/\/images.dog.ceo\/breeds\/boxer\/n02108089_1357.jpg"},
/ #
```

**ВНИМАНИЕ** Генерировать файл не надо, он уже есть в исходном наборе

Подключаемся в `bash` терминал контейнера
```shell
python3 upstart.py -s bash
```

Загрузим файл в Mongo с помощью утилиты mongoimport:

```json
/usr/bin/mongoimport --host ${APP_MONGO_HOST} --port ${APP_MONGO_PORT} --db pets --collection dogs --file /usr/share/data_store/raw_data/dogs.json
```

Результат выполнения команды
```json
2019-10-27T15:50:25.965+0000    connected to: mongo_host:27017
2019-10-27T15:50:25.999+0000    imported 100 documents
```

Проверим, что документы успешно загружены, подключившись к Mongo командой `/usr/bin/mongo ${APP_MONGO_HOST}:${APP_MONGO_PORT}/pets`:
```python
db.stats()
```

Результат

```json
{
	"db" : "pets",
	"collections" : 1,
	"views" : 0,
	"objects" : 100,
	"avgObjSize" : 115.46,
	"dataSize" : 11546,
	"storageSize" : 16384,
	"numExtents" : 0,
	"indexes" : 1,
	"indexSize" : 16384,
	"fsUsedSize" : 43341520896,
	"fsTotalSize" : 244529655808,
	"ok" : 1
}
```

Посмотрим на записи, которые появились в таблице
```json
db.dogs.find().limit(3)
```

Результат

```json
{ "_id" : ObjectId("5b5aad7b54c17bb03ac25e64"), "status" : "success", "message" : "https://images.dog.ceo/breeds/greyhound-italian/n02091032_9131.jpg" }
{ "_id" : ObjectId("5b5aad7b54c17bb03ac25e65"), "status" : "success", "message" : "https://images.dog.ceo/breeds/hound-afghan/n02088094_1534.jpg" }
{ "_id" : ObjectId("5b5aad7b54c17bb03ac25e66"), "status" : "success", "message" : "https://images.dog.ceo/breeds/chihuahua/n02085620_5093.jpg" }
```

## Группировка данных

Для группировки данных существует модификатор group - аналог GROUP BY в стандарте SQL. Его синтаксис:
```json
{ $group: { _id: <expression>, <field1>: { <accumulator1> : <expression1> }, ... } }
```

Этот модификатор оборачивается в конструкцию `db.dogs.aggregate([])`

Подключаемся в Mongo

```json
/usr/bin/mongo ${APP_MONGO_HOST}:${APP_MONGO_PORT}/pets
```

Применим к нашей игрушечной таблице `aggregate()`:

```python
db.dogs.aggregate([{$group: {_id: "$status"}}])
```

Это минимально допустимая конструкция, которая не делает ничего полезного, т.к. мы не указали агрегирующую функцию.
Усложним пример, добавив простой счётчик
```json
db.dogs.aggregate([{$group: {_id: "$status", dog_count: { $sum: 1 }}}])
```

Результат

```json
{ "_id" : "success", "dog_count" : 200 }
```

## Модификация полей.

Допустим, для предыдущего примера мы хотим посчитать не просто количество документов, а сумму длин поля $message.

Для этой задачи потребуется добавить к коллекции новое поле - message_len.

Строки в Mongo - объекты Javascript, то есть у них есть атрибут `length`. Таким образом нам нужно применить функцию length каждому полю message всех документов коллекции.
Для этого мы используем метод курсора forEach и вызовем метод update для каждого документа:

```json
db.dogs.find().forEach(function(doc){db.dogs.update({_id:doc._id}, {$set: {message_len: doc.message.length}})})
```

Теперь можно посчитать ещё один агрегат - сумму длин строк:

```json
db.dogs.aggregate([{$group: {_id: "$status", tag_count: { $sum: 1 }, descr_len: {$sum: "$message_len"}}}])
{ "_id" : "success", "tag_count" : 200, "descr_len" : 11845 }
```
