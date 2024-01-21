from dataclasses import dataclass
from redis import Redis
import os
import logging as log


@dataclass
class RedisConnectionConfig:
    host: str = os.getenv('REDIS_HOST') or 'localhost'
    port: int = 6379
    db: int = 1
    decode_responses: bool = True


@dataclass
class AuthManager:

    connection_config: RedisConnectionConfig = None
    refresh_token: str = ""

    def store(self):
        redis_conn = Redis(host=self.connection_config.host,
                           port=self.connection_config.port,
                           db=self.connection_config.db,
                           decode_responses=self.connection_config.decode_responses
                           )
        redis_conn.set("refresh_token", self.refresh_token)
        log.debug(f'Stored refresh token {self.refresh_token} in Redis')

        return {"refresh_token": "stored"}

    def fetch(self):
        redis_conn = Redis(host=self.connection_config.host,
                           port=self.connection_config.port,
                           db=self.connection_config.db,
                           decode_responses=self.connection_config.decode_responses
                           )
        self.refresh_token = redis_conn.get("refresh_token")
        log.debug(f'Fetched refresh token {self.refresh_token} from Redis')

        return {"refresh_token": self.refresh_token}
