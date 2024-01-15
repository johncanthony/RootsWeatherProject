
from ManagerAPI.api.managers.state_manager import StateManager


def test_valid_state():
    state_manager = StateManager()
    assert state_manager.valid_state("new") == True
    assert state_manager.valid_state("imgresolved") == True
    assert state_manager.valid_state("grabbed") == True
    assert state_manager.valid_state("packed") == True
    assert state_manager.valid_state("uploaded") == True
    assert state_manager.valid_state("error") == True
    assert state_manager.valid_state("jobs:INVALID") == False


def test_states():
    state_manager = StateManager()
    print(state_manager.states())
    assert state_manager.states() == {'new': 'jobs:NEW', 'imgresolved': 'jobs:IMGRESOLVED', 'grabbed': 'jobs:GRABBED',
                                      'packed': 'jobs:PACKED', 'uploaded': 'jobs:UPLOADED', 'error': 'jobs:ERROR'}
