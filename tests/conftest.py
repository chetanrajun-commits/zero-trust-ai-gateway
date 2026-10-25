"""Shared fixtures for the gateway test suite."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from gateway.guardrails import GuardrailsEngine
from gateway.main import app


@pytest.fixture
def client() -> TestClient:
    """Returns a FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def guardrails() -> GuardrailsEngine:
    """Returns a fresh GuardrailsEngine instance."""
    return GuardrailsEngine()
