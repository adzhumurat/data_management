# Mongo command line interface

Подключение к Mongo-серверу осуществляется с помощью утилиты Mongo (в докер-контейнере она уже установлена)

<pre>
/usr/bin/mongo ${APP_MONGO_HOST}:${APP_MONGO_PORT}
</pre>

Результат

<pre>
MongoDB shell version v4.0.0
connecting to: mongodb://mongo_host:27017/
MongoDB server version: 4.0.0
Welcome to the MongoDB shell.
For interactive help, type "help".
---

>
</pre>

В консоли существует множество команд


stats - статистика MongoDB

<pre>
db.stats()
</pre>

Результат

<pre>
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
</pre>

Создадим коллекцию документов

<pre>
use test_db
</pre>

Результат

<pre>
switched to db test_db
</pre>

Добавим в коллекцию документов один документ

<pre>
db.test_db.insert({name: 'Pepe', gender: 'm', weight: 40})
</pre>

Результат

<pre>
WriteResult({ "nInserted" : 1 })
</pre>

Снова посмотрим статистику по БД - мы увидим одну созданную коллеккцию:
<pre>
db.stats()
</pre>

Результат

<pre>
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
</pre>

Как видно, у нас в БД появилась новая коллекция и один объект. В любой момент мы можем проверить, какие объекты хранятся в БД:

<pre>
db.getCollectionNames()
</pre>

Результат

<pre>
[ "test_db" ]
</pre>

Для фильтрации записей используем find (аналог WHERE из SQL)

<pre>
db.test_db.find({'name': 'Pepe'})
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b56a66a64669cd544d5fd73"), "name" : "Pepe", "gender" : "m", "weight" : 40 }
</pre>

JSON, который передётся в функцию find называется "селектор". Селектор формирует набор документов из коллекции, которые отвечают уловиям, перечисленным в селектора.

Добавим новый документ в коллекцию с отличающимся набором полей:

<pre>
db.test_db.insert({name: 'Lolo', gender: 'f', home: 'Moscow', student: false})
</pre>

Результат

<pre>
WriteResult({ "nInserted" : 1 })
</pre>

Воспользуемся командой find(), которая является аналогом для SELECT в стандарте SQL.
<pre>
db.test_db.find()
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b56a66a64669cd544d5fd73"), "name" : "Pepe", "gender" : "m", "weight" : 40 }
{ "_id" : ObjectId("5b56b32e64669cd544d5fd74"), "name" : "Lolo", "gender" : "f", "home" : "Moscow", "student" : false }
</pre>

Мы добавили в нашу коллекцию новый домумент с другим набором полей. Такое добавление было бы невозможно в реляционной БД, где набор полей фиксируется в момент создания таблицы.

Для удаления записей используется функция .remove(), в которую нужно передать селектор
<pre>
db.test_db.remove({home: "Moscow"})
</pre>

Результат

<pre>
WriteResult({ "nRemoved" : 1 })
</pre>

Проверим, какие элементы остались в коллекции

<pre>
db.test_db.find()
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b56a66a64669cd544d5fd73"), "name" : "Pepe", "gender" : "m", "weight" : 40 }
</pre>

В селекторы можно передавать специальные операторы, которые эквивалентны условиям в WHERE запросов SQL:

<pre>
db.test_db.find({gender: 'm', weight: {$gt: 700}})
</pre>

Тут ничего не нашли - это ожидаемо. Поправим условие в селекторе:

<pre>
db.test_db.find({gender: 'm', weight: {$lt: 700}})
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b56a66a64669cd544d5fd73"), "name" : "Pepe", "gender" : "m", "weight" : 40 }
</pre>

Так, например, оператор $exists проверяет наличие у объекта того или иного поля. Внутри селектора условия можно объединять с помощью оператора $or
<pre>
db.test_db.find({$or: [{gender: 'm'}, {home: 'Moscow'}]})
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b56a66a64669cd544d5fd73"), "name" : "Pepe", "gender" : "m", "weight" : 40 }
{ "_id" : ObjectId("5b56b78664669cd544d5fd75"), "name" : "Lolo", "gender" : "f", "home" : "Moscow", "student" : false }
</pre>

## Обновление записей

Обновление производится функцией update, попробуем её применить

<pre>
db.test_db.update({home: 'Moscow'},{student: true})
</pre>

Результат

<pre>
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
</pre>

Проверим, что новый документ появился в коллекции
<pre>
db.test_db.find({home: 'Moscow'})
</pre>

Ничего не нашли, что случилось? Выведем все документы коллекции
<pre>
db.test_db.find()
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b56a66a64669cd544d5fd73"), "name" : "Pepe", "gender" : "m", "weight" : 40 }
{ "_id" : ObjectId("5b56b78664669cd544d5fd75"), "student" : true }
</pre>

Фунция update не просто изменила это поля, а переписала весь документ. Чтобы такого не произошло, нужно использовать модификатор $set

Вернём нашу запись на место
<pre>
db.test_db.insert({name: 'Lolo', gender: 'f', home: 'Moscow', student: false})
</pre>

Результат

<pre>
WriteResult({ "nInserted" : 1 })
</pre>

Проведём правильный update
<pre>
db.test_db.update({home: 'Moscow'}, {$set: {student: true}})
</pre>

Результат

<pre>
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
</pre>


Проверим, что всё успешно
<pre>
db.test_db.find()
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b571bf081d67789509607f1"), "name" : "Lolo", "gender" : "f", "home" : "Moscow", "student" : true }
</pre>


Третий параметр в методе update позволяет создать запись, если она отсутствует - т.н. upsert (UPDATE + INSERT)


Попробуем выполнить update записи, которой нет
<pre>
db.test_db.update({home: 'Perm'}, {$set: {student: false}})
</pre>

Результат

<pre>
WriteResult({ "nMatched" : 0, "nUpserted" : 0, "nModified" : 0 })
</pre>

Как изменилась коллекция? Никак =[
<pre>
db.test_db.find()
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b571bf081d67789509607f1"), "name" : "Lolo", "gender" : "f", "home" : "Moscow", "student" : true }
</pre>

Попробуем функционал UPSERT:
<pre>
db.test_db.update({home: 'Perm'}, {$set: {student: false}}, true)
</pre>

Результат

<pre>
WriteResult({
	"nMatched" : 0,
	"nUpserted" : 1,
	"nModified" : 0,
	"_id" : ObjectId("5b57207bbff183a0a45dcfb3")
})
</pre>

Проверим, как изменилась коллекция
<pre>
db.test_db.find()
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b571bf081d67789509607f1"), "name" : "Lolo", "gender" : "f", "home" : "Moscow", "student" : true }
{ "_id" : ObjectId("5b57207bbff183a0a45dcfb3"), "home" : "Perm", "student" : false }
</pre>

По умолчанию будет обновлён один из документов, попадающих под условия селектора. Чётвёртый параметр команды позволяет осуществлять массовую вставку (обновление) документов.

Есть другие модификаторы, например $inc (увеличивает скаляр) или $push (добавляет в массив) - о них можно почитать
в документации по [Mongo](https://docs.mongodb.com/manual/reference/operator/update/)

# Mongo - продвинутые техники

Отсутствуют джойны. Чтобы как-то моделировать джойны предлагается особенным образом формировать документы - чтобы сохранять связи между различными коллекциями

<pre>
db.posts.insert({day: 'Wed', author: ObjectId("5b571bf081d67789509607f1")})
db.posts.insert({day: 'Sat', author: ObjectId("5b571bf081d67789509607f1")})
db.posts.insert({day: 'Sat', author: ObjectId("5b57207bbff183a0a45dcfb3")})
</pre>

Проверим, что записалось в БД
<pre>
db.posts.find()
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b57392b81d67789509607f2"), "day" : "Wed", "author" : ObjectId("5b571bf081d67789509607f1") }
{ "_id" : ObjectId("5b57393481d67789509607f3"), "day" : "Sat", "author" : ObjectId("5b571bf081d67789509607f1") }
{ "_id" : ObjectId("5b57394381d67789509607f4"), "day" : "Sat", "author" : ObjectId("5b57207bbff183a0a45dcfb3") }
</pre>

Вместо джойна используем find по полю ObjectId

<pre>
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")})
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b57392b81d67789509607f2"), "day" : "Wed", "author" : ObjectId("5b571bf081d67789509607f1") }
{ "_id" : ObjectId("5b57393481d67789509607f3"), "day" : "Sat", "author" : ObjectId("5b571bf081d67789509607f1") }
</pre>

Пo умолчанию возвращаются все поля документа. Это поведение можно изменить:
<pre>
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")}, {day: 1})
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b57392b81d67789509607f2"), "day" : "Wed" }
{ "_id" : ObjectId("5b57393481d67789509607f3"), "day" : "Sat" }
</pre>

Служебное поле _id возвращается всегда - его можно выключить в явном виде

<pre>
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")}, {day: 1, _id: 0})
</pre>

Результат

<pre>
{ "day" : "Wed" }
{ "day" : "Sat" }
</pre>

В остальных случаях включение и исключение полей нельзя смешивать.

Порядок выдачи изменяется командой .sort():

<pre>
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")}, {day: 1, _id: 0}).sort({day: 1})
</pre>

Результат

<pre>
{ "day" : "Sat" }
{ "day" : "Wed" }
</pre>

или в обратном порядке

<pre>
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")}, {day: 1, _id: 0}).sort({day: -1})
</pre>

Результат

<pre>
{ "day" : "Wed" }
{ "day" : "Sat" }
</pre>

Так же можно управлять количеством записей в выдаче и смещением от начала списка

Полная выдача:
<pre>
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")}, {day: 1, _id: 0}).sort({day: -1})
</pre>

Результат

<pre>
{ "day" : "Wed" }
{ "day" : "Sat" }
</pre>

Задаём смещение
<pre>
db.posts.find({author: ObjectId("5b571bf081d67789509607f1")}, {day: 1, _id: 0}).sort({day: -1}).limit(2).skip(1)
</pre>

Результат

<pre>
{ "day" : "Sat" }
</pre>

Гибкость курсора позволяет управлять нагрузкой на Mongo, так как курсор умеет делать смещения без непосредственного чтения записей

## Загрузка JSON

Для загрузки JSON выполним скрипт формирования JSON - это будут случайные картинки собачек, получаемых по API

<pre>
rm -f test.json; for i in $(seq 100 $END); do curl "https://dog.ceo/api/breeds/image/random">>test.json; done;
</pre>

На выходе получаем JSON-файл
<pre>
head test.json;
</pre>

Результат

<pre>
{"status":"success","message":"https:\/\/images.dog.ceo\/breeds\/weimaraner\/n02092339_1013.jpg"},
{"status":"success","message":"https:\/\/images.dog.ceo\/breeds\/basenji\/n02110806_5971.jpg"},
{"status":"success","message":"https:\/\/images.dog.ceo\/breeds\/dingo\/n02115641_5815.jpg"},
{"status":"success","message":"https:\/\/images.dog.ceo\/breeds\/corgi-cardigan\/n02113186_10475.jpg"},
{"status":"success","message":"https:\/\/images.dog.ceo\/breeds\/boxer\/n02108089_1357.jpg"},
/ #
</pre>

**ВНИМАНИЕ** Генерировать файл не надо, он уже есть в исходном наборе

Загрузим файл в Mongo с помощью утилиты mongoimport:

<pre>
/usr/bin/mongoimport --host ${APP_MONGO_HOST} --port ${APP_MONGO_PORT} --db pets --collection dogs --file /usr/share/raw_data/dogs.json
</pre>

Результат выполнения команды
<pre>
2019-10-27T15:50:25.965+0000    connected to: mongo_host:27017
2019-10-27T15:50:25.999+0000    imported 100 documents
</pre>

Проверим, что документы успешно загружены, подключившись к Mongo ` /usr/bin/mongo ${APP_MONGO_HOST}:${APP_MONGO_PORT}/pets`:
<pre>
use pets
db.stats()
</pre>

Результат

<pre>
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
</pre>

Посмотрим на записи, которые появились в таблице
<pre>
use pets
db.dogs.find().limit(3)
</pre>

Результат

<pre>
{ "_id" : ObjectId("5b5aad7b54c17bb03ac25e64"), "status" : "success", "message" : "https://images.dog.ceo/breeds/greyhound-italian/n02091032_9131.jpg" }
{ "_id" : ObjectId("5b5aad7b54c17bb03ac25e65"), "status" : "success", "message" : "https://images.dog.ceo/breeds/hound-afghan/n02088094_1534.jpg" }
{ "_id" : ObjectId("5b5aad7b54c17bb03ac25e66"), "status" : "success", "message" : "https://images.dog.ceo/breeds/chihuahua/n02085620_5093.jpg" }
</pre>

## Группировка данных

Для группировки данных существует модификатор group - аналог GROUP BY в стандарте SQL. Его синтаксис:
<pre>
{ $group: { _id: <expression>, <field1>: { <accumulator1> : <expression1> }, ... } }
</pre>

Этот модификатор оборачивается в конструкцию *db.dogs.aggregate([])*

Применим к нашей игрушечной таблице

<pre>
/usr/bin/mongo ${APP_MONGO_HOST}:${APP_MONGO_PORT}/pets
db.dogs.aggregate([{$group: {_id: "$status"}}])
</pre>

Это минимально допустимая конструкция, которая не делает ничего полезного, т.к. мы не указали агрегирующую функцию.
Усложним пример, добавив простой счётчик
<pre>
db.dogs.aggregate([{$group: {_id: "$status", dog_count: { $sum: 1 }}}])
</pre>

Результат

<pre>
{ "_id" : "success", "dog_count" : 200 }
</pre>

## Модификация полей.

Допустим, для предыдущего примера мы хотим посчитать не просто количество документов, а сумму длинн поля $message.

Для этой задачи потребуется добавить к коллеции новое поле - message_len.

Строки в Mongo - объекты Javascript, то есть у них есть атрибут length. Таким образом нам нужно применить функцию length каждому полю message всех документов коллекции.
Для этого мы используем метод курсора forEach и вызовем метод update для каждого документа:

<pre>
db.dogs.find().forEach(function(doc){db.dogs.update({_id:doc._id}, {$set: {message_len: doc.message.length}})})
</pre>

Теперь можно посчитать ещё один агрегат - сумму длин строк:

<pre>
db.dogs.aggregate([{$group: {_id: "$status", tag_count: { $sum: 1 }, descr_len: {$sum: "$message_len"}}}])
{ "_id" : "success", "tag_count" : 200, "descr_len" : 11845 }
</pre>
