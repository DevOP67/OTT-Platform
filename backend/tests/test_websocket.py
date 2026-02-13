import pytest
from websocket_manager import manager

@pytest.mark.asyncio
async def test_connection_manager():
    # Test manager initialization
    assert len(manager.active_connections) == 0
    assert len(manager.session_states) == 0

def test_session_state_storage():
    session_id = 'test-session'
    state = {'position': 100, 'is_playing': True}
    
    manager.session_states[session_id] = state
    
    assert session_id in manager.session_states
    assert manager.session_states[session_id]['position'] == 100
