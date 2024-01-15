from dataclasses import dataclass, asdict

'''
A job can only be in a one discrete state at once. That state will correspond to a list queue
in Redis.

States: NEW -> IMGRESOLVED -> GRABBED -> PACKED -> UPLOADED || ERROR
'''


@dataclass
class StateManager:

    new: str = "jobs:NEW"
    imgresolved: str = "jobs:IMGRESOLVED"
    grabbed: str = "jobs:GRABBED"
    packed: str = "jobs:PACKED"
    uploaded: str = "jobs:UPLOADED"
    error: str = "jobs:ERROR"

    def __getitem__(self, item):
        return getattr(self, item)

    def valid_state(self, state: str):
        return state in asdict(self)

    def states(self):
        return asdict(self)
