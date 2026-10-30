import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.game_engine import game_engine
from app.models.game_schemas import IndictmentRequest

@pytest.mark.asyncio
async def test_case_dossier():
    dossier = game_engine.get_dossier()
    assert dossier.case_number == "CASE-1031"
    assert len(dossier.suspects) == 4
    assert len(dossier.evidence_locker) == 4

@pytest.mark.asyncio
async def test_interrogate_phantom_socket():
    res = await game_engine.interrogate(
        suspect_id="phantom_socket",
        message="Did you bind port 666?",
        presented_evidence_id="core_dump"
    )
    assert res.suspect_id == "phantom_socket"
    assert res.tension_level >= 80
    assert "0x7FFFDEADBEEF" in res.reply or "deadbeef" in res.reply.lower()

@pytest.mark.asyncio
async def test_indictment_guilty():
    req = IndictmentRequest(
        accused_suspect_id="phantom_socket",
        murder_weapon="Buffer Overflow 0xDEADBEEF",
        exorcism_command="kill -9 666",
        notes="Port 666 injected raw bytes into stack buffer."
    )
    res = game_engine.evaluate_indictment(req)
    assert res.verdict == "GUILTY_EXORCISED"
    assert res.success is True
    assert res.score == 100

@pytest.mark.asyncio
async def test_indictment_wrongful():
    req = IndictmentRequest(
        accused_suspect_id="garbage_collector",
        murder_weapon="Memory Leak",
        exorcism_command="pkill -f gc",
        notes="GC swept the memory."
    )
    res = game_engine.evaluate_indictment(req)
    assert res.verdict == "WRONGFUL_CONVICTION"
    assert res.success is False
    assert res.score < 50

@pytest.mark.asyncio
async def test_game_api_endpoints():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Get case
        r1 = await ac.get("/api/game/case")
        assert r1.status_code == 200
        data = r1.json()
        assert data["case_number"] == "CASE-1031"

        # 2. Interrogate
        r2 = await ac.post("/api/game/interrogate", json={
            "suspect_id": "systemd",
            "message": "Where were you at 03:42:19?",
            "presented_evidence_id": "syslog_corrupt"
        })
        assert r2.status_code == 200
        interrogate_data = r2.json()
        assert "reply" in interrogate_data

        # 3. Indict
        r3 = await ac.post("/api/game/indict", json={
            "accused_suspect_id": "phantom_socket",
            "murder_weapon": "Buffer Overflow",
            "exorcism_command": "kill -9 666"
        })
        assert r3.status_code == 200
        indict_data = r3.json()
        assert indict_data["success"] is True
