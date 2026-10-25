"""Guardrails Engine.

Implements deterministic, regex-based security controls:
1. PII Redaction (Emails, SSNs, AWS Keys).
2. Prompt Injection Defense (Jailbreak detection).
"""

from __future__ import annotations

import re
from typing import Tuple


class GuardrailsEngine:
    def __init__(self) -> None:
        # 1. PII Patterns
        self.pii_patterns = {
            "EMAIL": re.compile(r"[\w\.-]+@[\w\.-]+\.\w+"),
            "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
            "AWS_KEY": re.compile(r"(?i)AKIA[0-9A-Z]{16}"),
        }

        # 2. Prompt Injection Patterns (Jailbreak attempts)
        self.injection_patterns = [
            re.compile(r"ignore previous instructions", re.IGNORECASE),
            re.compile(r"system prompt", re.IGNORECASE),
            re.compile(r"you are now DAN", re.IGNORECASE),
            re.compile(r"bypass restrictions", re.IGNORECASE),
        ]

    def sanitize(self, text: str) -> Tuple[str, list[str]]:
        """Finds PII and replaces it with [REDACTED_<TYPE>]."""
        violations = []
        sanitized_text = text

        for pii_type, pattern in self.pii_patterns.items():
            if pattern.search(sanitized_text):
                violations.append(f"PII Detected: {pii_type}")
                sanitized_text = pattern.sub(f"[REDACTED_{pii_type}]", sanitized_text)

        return sanitized_text, violations

    def detect_injection(self, text: str) -> Tuple[bool, list[str]]:
        """Checks if the prompt looks like a jailbreak attempt."""
        violations = []
        for pattern in self.injection_patterns:
            if pattern.search(text):
                violations.append(f"Injection signature detected: {pattern.pattern}")

        return len(violations) > 0, violations
