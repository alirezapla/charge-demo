rs.initiate(
    {
        _id: "shard2",
        version: 1,
        members: [
            { _id: 0, host: "shard2a:27017" },
            { _id: 1, host: "shard2b:27017" },
        ],
        settings: {
            electionTimeoutMillis: 10000,
        }
    }
)