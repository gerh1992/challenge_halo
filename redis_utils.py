from datetime import datetime
import logging
import os
import redis


class RedisUtils():

    REDIS_HOST = os.getenv("FLASK_REDIS_HOST", "localhost")
    REDIS_PW = os.getenv("FLASK_REDIS_PASSWORD", "123456")
    REDIS_PORT = os.getenv("FLASK_REDIS_PORT", "6379")

    def __init__(self):
        self._con = redis.Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            password=self.REDIS_PW,
            decode_responses=True
        )
        self._first_health_check = None
        self._latest_health_check = None
        self.check_health()

    def check_health(self):
        # Check health status on redis, ping is the recommended way by redis
        try:
            logging.debug("Sending redis ping...")
            self._con.ping()
            logging.debug("Ping command succesful")
            if not self._first_health_check:
                self._first_health_check = datetime.today()
            self._latest_health_check = datetime.today()
            return True
        except redis.exceptions.RedisError:
            logging.critical("Redis ping command failed, resetting healtcheck metrics")
            self._first_health_check = None
            self._latest_health_check = None
            return False

    def get_total_uptime(self):
        # Total uptime is calculated by substracting the last time we checked against the first time.
        if not self._latest_health_check or not self._first_health_check:
            return 0.0
        total_uptime = (self._latest_health_check - self._first_health_check).total_seconds()
        return total_uptime / 60 / 60  # Transform to hours

    def get_and_delete_key(self, key):
        return self._con.getdel(key)

    def set(self, key, value):
        val = self._con.get(key)
        if val:
            logging.debug(f"key: {key} exists, value:{val}")
            return False
        self._con.set(key, value, nx=True)
        return True

    def db_size(self):
        """
        Returns the total amount of keys stored in redis or -1 if there is an issue
        """
        try:
            return self._con.dbsize()
        except redis.exceptions.RedisError as err:
            logging.critical(err)
            return -1

    def flushall(self):
        logging.debug("Removing all keys from redis")
        return self._con.flushall()
