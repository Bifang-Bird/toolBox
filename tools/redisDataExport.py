import redis

# r = redis.Redis(host='10.2.4.126', port=6379, db=0)
# pool = redis.ConnectionPool(host='10.2.4.126', port=6379)
# r = redis.Redis(connection_pool=pool)
pool = redis.ConnectionPool(host='10.2.4.126', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
pipe = r.pipeline()
pipe.hget("globalid", "LVVDB27BXKD144896")
result = pipe.execute()
print (result)
