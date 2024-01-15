from dataclasses import dataclass


@dataclass
class RedisConnectionConfig():
    host: str = "localhost"
    port: int = 6379
    db: int = 1
    decode_responses: bool = True
