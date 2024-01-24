sh.enableSharding("demo_mongodb")
sh.shardCollection('demo_mongodb.charge', { key: "hashed" })
sh.shardCollection('demo_mongodb.user', { username: "hashed" })
sh.shardCollection('demo_mongodb.transactions', { transactionId: "hashed" })
