#!/bin/bash

docker-compose -f docker-compose-db.yml exec router sh -c "mongosh < scripts/status.js"
