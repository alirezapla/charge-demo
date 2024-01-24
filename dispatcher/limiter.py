from limits import RateLimitItem, RateLimitItemPerMinute, storage, strategies
from decouple import config

storage = storage.RedisStorage(config("REDIS_URL"))
throttler = strategies.MovingWindowRateLimiter(storage)


def hit(key: str, rate_per_minute: int, cost: int = 1) -> bool:
    item = rate_limit_item_for(rate_per_minute=rate_per_minute)
    is_hit = throttler.hit(item, key, cost=cost)
    return is_hit


def rate_limit_item_for(rate_per_minute: int) -> RateLimitItem:
    return RateLimitItemPerMinute(rate_per_minute)
