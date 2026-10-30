import pytest
from app.services.llm_engine import llm_engine

@pytest.mark.asyncio
async def test_silent_exception_swallow():
    haunted_code = """
def process_user_data(data):
    try:
        data = parse_payload(data)
    except:
        pass
    return data
"""
    result = await llm_engine.exorcise_code(haunted_code, "user_service.py", "python")
    assert result.haunted_score > 20
    assert len(result.anomalies_found) >= 1
    assert any("Silent Exception" in a.ghost_pattern or "Black Hole" in a.ghost_pattern for a in result.anomalies_found)
    assert "logger" in result.unified_diff or "logging" in result.unified_diff or "except Exception" in result.unified_diff

@pytest.mark.asyncio
async def test_mutable_default_argument():
    code = """
def append_item(item, target_list=[]):
    target_list.append(item)
    return target_list
"""
    result = await llm_engine.exorcise_code(code, "utils.py", "python")
    assert any("Mutable Default" in a.ghost_pattern or "State Bleed" in a.ghost_pattern for a in result.anomalies_found)
    assert "=None" in result.purified_code

@pytest.mark.asyncio
async def test_js_zombie_event_listener():
    code = """
function initWatcher() {
    window.addEventListener('resize', handleResize);
}
"""
    result = await llm_engine.exorcise_code(code, "watcher.js", "javascript")
    assert any("Zombie Event Listener" in a.ghost_pattern for a in result.anomalies_found)
