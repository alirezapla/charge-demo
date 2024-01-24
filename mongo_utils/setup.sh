#!/bin/bash

docker-compose exec config1 sh -c "mongosh  < /scripts/configserver.js"
echo 'configed'
sleep 5
docker-compose exec shard1a sh -c "mongosh  < /scripts/shard1.js"
docker-compose exec shard2a sh -c "mongosh  < /scripts/shard2.js"
echo 'shards initiliazed'
sleep 5
docker-compose exec router sh -c "mongosh  < /scripts/router.js"
sleep 5
docker-compose exec router sh -c "mongosh < /scripts/enable.js"
echo 'ready'