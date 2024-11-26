from core.settings.base import REDIS_HOST, REDIS_PORT, REDIS_DB
from redis import Redis


redis = Redis(host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB)
