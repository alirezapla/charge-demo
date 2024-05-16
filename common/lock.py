import redis
import time

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def acquire_lock(lock_name, acquire_timeout=10, lock_timeout=10):
    identifier = str(uuid.uuid4())
    end = time.time() + acquire_timeout
    lock = f'lock:{lock_name}'

    while time.time() < end:
        if redis_client.set(lock, identifier, ex=lock_timeout, nx=True):
            return identifier
        elif not redis_client.ttl(lock):
            redis_client.expire(lock, lock_timeout)
        time.sleep(0.001)
    return False

def release_lock(lock_name, identifier):
    lock = f'lock:{lock_name}'
    with redis_client.pipeline() as pipe:
        while True:
            try:
                pipe.watch(lock)
                if pipe.get(lock).decode('utf-8') == identifier:
                    pipe.multi()
                    pipe.delete(lock)
                    pipe.execute()
                    return True
                pipe.unwatch()
                break
            except redis.WatchError:
                continue
    return False
