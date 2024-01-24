#!/bin/bash

docker-compose exec router sh -c "mongosh < scripts/status.js"
