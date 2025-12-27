import redis
from typing import Optional

class RedisClient:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """
        初始化 Redis 客户端连接。
        :param host: Redis 服务器地址，默认为 localhost。
        :param port: Redis 端口，默认为 6379。
        :param db: Redis 数据库，默认为 0。
        """
        self.host = host
        self.port = port
        self.db = db
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db)

    def set(self, key: str, value: str, ex: Optional[int] = None):
        """
        设置 Redis 键值对。
        :param key: 键名。
        :param value: 值。
        :param ex: 可选，设置过期时间（单位秒）。
        """
        try:
            self.client.set(key, value, ex=ex)
            print(f"Successfully set {key} = {value}")
        except redis.RedisError as e:
            print(f"Error setting value in Redis: {e}")

    def get(self, key: str) -> Optional[str]:
        """
        获取 Redis 中指定键的值。
        :param key: 键名。
        :return: 键对应的值，若不存在返回 None。
        """
        try:
            value = self.client.get(key)
            if value is not None:
                return value.decode('utf-8')  # 解码为字符串
            return None
        except redis.RedisError as e:
            print(f"Error getting value from Redis: {e}")
            return None

    def delete(self, key: str) -> bool:
        """
        删除 Redis 中指定键。
        :param key: 键名。
        :return: 返回是否成功删除。
        """
        try:
            result = self.client.delete(key)
            return result > 0  # 如果返回 0，表示键不存在
        except redis.RedisError as e:
            print(f"Error deleting key in Redis: {e}")
            return False

    def exists(self, key: str) -> bool:
        """
        检查 Redis 中是否存在指定键。
        :param key: 键名。
        :return: 如果键存在，返回 True；否则返回 False。
        """
        try:
            return self.client.exists(key)
        except redis.RedisError as e:
            print(f"Error checking key existence in Redis: {e}")
            return False

    def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """
        自增 Redis 键的值。
        :param key: 键名。
        :param amount: 自增的数量，默认为 1。
        :return: 新的值，若键不存在会创建并设置为 `amount`。
        """
        try:
            return self.client.incr(key, amount)
        except redis.RedisError as e:
            print(f"Error incrementing value in Redis: {e}")
            return None

    def decrement(self, key: str, amount: int = 1) -> Optional[int]:
        """
        自减 Redis 键的值。
        :param key: 键名。
        :param amount: 自减的数量，默认为 1。
        :return: 新的值，若键不存在会创建并设置为 `-amount`。
        """
        try:
            return self.client.decr(key, amount)
        except redis.RedisError as e:
            print(f"Error decrementing value in Redis: {e}")
            return None

    def flush_db(self):
        """
        清空当前数据库中的所有键值对。
        """
        try:
            self.client.flushdb()
            print("Flushed the current Redis database.")
        except redis.RedisError as e:
            print(f"Error flushing Redis database: {e}")

    def close(self):
        """
        关闭 Redis 连接。
        """
        try:
            self.client.close()
            print("Redis connection closed.")
        except redis.RedisError as e:
            print(f"Error closing Redis connection: {e}")


if __name__ == "__main__":
    redis_client = RedisClient(host='localhost', port=6379, db=0)
    redis_client.set('name', 'John Doe')
    name = redis_client.get('name')
    print(f"Name: {name}")
    redis_client.increment('counter', 10)
    exists = redis_client.exists('name')
    print(f"Does 'name' exist? {exists}")
    redis_client.delete('name')
    redis_client.flush_db()
    redis_client.close()

