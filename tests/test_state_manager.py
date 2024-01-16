
from ManagerAPI.api.managers.state_manager import StateManager


def test_valid_state():
    state_manager = StateManager()
    states = [("new", True),
              ("imgresolved", True),
              ("grabbed", True),
              ("packed", True),
              ("uploaded", True),
              ("error", True),
              ("invalid", False)]

    for state in states:
        assert state_manager.valid_state(state[0]) is state[1]


def test_states():
    state_manager = StateManager()
    print(state_manager.states())
    assert state_manager.states() == {
                                      'new': 'jobs:NEW',
                                      'imgresolved': 'jobs:IMGRESOLVED',
                                      'grabbed': 'jobs:GRABBED',
                                      'packed': 'jobs:PACKED',
                                      'uploaded': 'jobs:UPLOADED',
                                      'error': 'jobs:ERROR'
                                      }
