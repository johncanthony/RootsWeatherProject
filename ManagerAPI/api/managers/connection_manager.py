from dataclasses import dataclass
from redis import Redis


@dataclass
class RedisConnectionConfig:
    host: str = "redis.home"
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

        return {"refresh_token": "stored"}

    def fetch(self):
        redis_conn = Redis(host=self.connection_config.host,
                           port=self.connection_config.port,
                           db=self.connection_config.db,
                           decode_responses=self.connection_config.decode_responses
                           )
        self.refresh_token = redis_conn.get("refresh_token")

        return {"refresh_token": self.refresh_token}
