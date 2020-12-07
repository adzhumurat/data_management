db.stats()

use movie

db.stats()

// Запрос 1
db["tags"].count()
db["tags"].aggregate([{ $count: "tsags_count" }])

// Запрос 2
db["tags"].count({ "tag_name": "Adventure" })
db["tags"].aggregate([{ $match: { "tag_name": "Adventure" } }, { $count: "adventure_count" }])

// Запрос 3
db["tags"].aggregate([{ $group: {_id: "$tag_name", count: { $sum: 1 } } }, { $sort: { count:-1 } }, { $limit: 3 }])


// Запрос 1
db.tags.count()
db.tags.aggregate([{ $count: "tsags_count" }])

// Запрос 2
db.tags.count({ "tag_name": "Adventure" })
db.tags.aggregate([{ $match: { "tag_name": "Adventure" } }, { $count: "adventure_count" }])

// Запрос 3
db.tags.aggregate([{ $group: {_id: "$tag_name", count: { $sum: 1 } } }, { $sort: { count:-1 } }, { $limit: 3 }])
