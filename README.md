# Charge and Customer Services demo

### Overview

## services

#### Architecture

![alt text](https://github.com/alirezapla/charge-demo/blob/main/reports/architecture_high_level.png)

#### Technology Stack

`python` ,`fastapi`, `rabbitmq`, `redis`, `mongodb`

Configuration

RABBITMQ_URL

MONGODB_URL

REDIS_URL

****

![alt text](https://github.com/minhhungit/mongodb-cluster-docker-compose/blob/master/images/sharding-and-replica-sets.png)

first, run services by

```python
docker-compose up -d
docker-compose -f docker-compose-db.yml up -d
```
then run `setup.sh`

```bash
sh mongo_utils/setup.sh
```
ready to use
