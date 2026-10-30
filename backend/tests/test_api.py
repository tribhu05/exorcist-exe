import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_api_status():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert data["app_name"] == "PHANTOM//SHELL"
        assert data["airgap_verified"] is True

@pytest.mark.asyncio
async def test_api_autopsy_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "command": "python script.py",
            "exit_code": 1,
            "stdout": "",
            "stderr": "ModuleNotFoundError: No module named 'numpy'"
        }
        response = await ac.post("/api/autopsy", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "anomaly_detected"
        assert "pip install numpy" in data["suggested_command"]

@pytest.mark.asyncio
async def test_api_exorcist_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "code": "def run():\n    try:\n        do_work()\n    except:\n        pass",
            "filename": "worker.py",
            "language": "python"
        }
        response = await ac.post("/api/exorcist", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["haunted_score"] > 0
        assert len(data["anomalies_found"]) > 0

@pytest.mark.asyncio
async def test_api_grimoire_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/grimoire")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
