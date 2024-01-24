#!/bin/bash
docker-compose exec router sh -c "mongosh  < /scripts/enAuth.js"
