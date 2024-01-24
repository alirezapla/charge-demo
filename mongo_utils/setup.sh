#!/bin/bash

docker-compose -f docker-compose-db.yml exec config1 sh -c "mongosh  < /scripts/configserver.js"
echo 'configed'
echo "wait please"
sleep 5
docker-compose -f docker-compose-db.yml exec shard1a sh -c "mongosh  < /scripts/shard1.js"
docker-compose -f docker-compose-db.yml exec shard2a sh -c "mongosh  < /scripts/shard2.js"
echo 'shards initiliazed'
echo "wait please"
sleep 5
docker-compose -f docker-compose-db.yml exec router sh -c "mongosh  < /scripts/router.js"
echo "wait please"
sleep 5
docker-compose -f docker-compose-db.yml exec router sh -c "mongosh < /scripts/enable.js"
echo 'ready'