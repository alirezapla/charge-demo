# Charge and Customer Services demo

### Overview
World Cup Discount Code Distribution System
Overview

This project is designed to distribute discount codes during the halftime of the World Cup finals. The goal is to distribute a set of discount codes with a total value of around 1 million units. The system is built to handle high traffic loads, ensuring that all users can receive their discount codes efficiently and reliably.
Features

    High Availability: Designed to withstand high traffic loads and ensure continuous availability.
    Scalability: Can scale horizontally to manage increasing user demands.
    Efficiency: Ensures quick and efficient distribution of discount codes.
    Security: Prevents abuse and ensures that each user can only claim one discount code.

Components

    Backend: The core logic for handling discount code requests and distributing them efficiently.
    Database: Stores information about the discount codes and tracks which codes have been claimed.
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
