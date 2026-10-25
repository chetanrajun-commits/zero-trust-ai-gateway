"""Pydantic models for API request/response validation."""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """Incoming request from a client application."""
    model: str = "gpt-4o"
    messages: list[Message]
    user_id: str = Field(description="Used for FinOps token tracking")


class SecurityReport(BaseModel):
    """Detailed telemetry on what the gateway blocked or modified."""
    pii_redacted: bool = False
    injection_blocked: bool = False
    violations: list[str] = []


class ChatResponse(BaseModel):
    """The sanitized response returned to the client."""
    reply: str
    security_report: SecurityReport
