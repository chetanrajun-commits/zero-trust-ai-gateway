# Zero-Trust AI Gateway

> A high-performance reverse proxy that enforces PII redaction, prompt injection defence, and token budgets for LLM APIs.

[![CI](https://github.com/chetanrajun-commits/zero-trust-ai-gateway/actions/workflows/ci.yml/badge.svg)](https://github.com/chetanrajun-commits/zero-trust-ai-gateway/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

---

## The Problem

Enterprises want to use LLMs, but InfoSec teams are terrified of data leakage (pasting customer PII or AWS keys into ChatGPT) and Prompt Injection attacks. Furthermore, there is zero visibility into which department is burning the most API tokens.

This repository is a **reference implementation** of the fix: a centralised Zero-Trust Gateway that sits between your applications and the LLM providers. 

## What it does

1. **Prompt Injection Defence:** Blocks malicious jailbreak attempts (e.g., "Ignore previous instructions") before they hit the model.
2. **PII Redaction:** Automatically detects and redacts Emails, SSNs, and AWS Keys from the prompt before it leaves your network.
3. **Deterministic:** Built with high-speed, compiled Regex. Zero machine learning dependencies required. 

---

## Demo

Because this is a FastAPI application, the demo simulates a client sending malicious requests through the gateway:

```bash
pip install -e .
python -m gateway.demo
