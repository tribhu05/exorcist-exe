import pytest
from app.services.llm_engine import llm_engine

@pytest.mark.asyncio
async def test_nominal_exit():
    autopsy = await llm_engine.autopsy_command(
        command="echo 'hello world'",
        exit_code=0,
        stdout="hello world\n",
        stderr=""
    )
    assert autopsy.status == "nominal"
    assert autopsy.severity == "LOW"

@pytest.mark.asyncio
async def test_port_conflict_autopsy():
    autopsy = await llm_engine.autopsy_command(
        command="npm run dev",
        exit_code=1,
        stdout="",
        stderr="Error: listen EADDRINUSE: address already in use :::3000"
    )
    assert autopsy.status == "anomaly_detected"
    assert "Zombie Port Conflict" in autopsy.ghost_type
    assert "3000" in autopsy.suggested_command

@pytest.mark.asyncio
async def test_missing_module_autopsy():
    autopsy = await llm_engine.autopsy_command(
        command="python app.py",
        exit_code=1,
        stdout="",
        stderr="ModuleNotFoundError: No module named 'fastapi'"
    )
    assert autopsy.status == "anomaly_detected"
    assert "Missing Module" in autopsy.ghost_type
    assert "pip install fastapi" in autopsy.suggested_command

@pytest.mark.asyncio
async def test_oom_reaper_autopsy():
    autopsy = await llm_engine.autopsy_command(
        command="./heavy_job",
        exit_code=137,
        stdout="",
        stderr="Killed: out of memory"
    )
    assert autopsy.status == "anomaly_detected"
    assert "OOM" in autopsy.ghost_type
    assert autopsy.severity == "CRITICAL"
