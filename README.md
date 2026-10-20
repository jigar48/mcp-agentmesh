# 🕸️ MCP Agent Mesh (`mcp-agent-mesh`)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Engine: Google Gemini](https://img.shields.io/badge/LLM-Google%20Gemini%202.5-orange.svg)](https://ai.google.dev/)
[![State: SQLAlchemy](https://img.shields.io/badge/Persistence-SQLAlchemy%20%2B%20SQLite-red.svg)](https://www.sqlalchemy.org/)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-buildwithjigar-FFDD00?logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/buildwithjigar)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Jigar%20Prajapati-0A66C2?logo=linkedin)](https://linkedin.com/in/jigar48)

> **Autonomous, single-file multi-agent engineering utility coordinating specialized AI sub-agents locally using Google Gemini and structured SQLAlchemy state persistence.**

---

## 📌 Table of Contents
- [Executive Overview](#-executive-overview)
- [Why `mcp-agent-mesh`?](#-why-mcp-agent-mesh)
- [System Architecture](#-system-architecture)
- [The Autonomous Agent Triad](#-the-autonomous-agent-triad)
- [Prerequisites & Installation](#-prerequisites--installation)
- [Quickstart Guide](#-quickstart-guide)
- [CLI Command Reference](#-cli-command-reference)
- [Python SDK Programmatic Usage](#-python-sdk-programmatic-usage)
- [SQLite Schema & Persistence](#-sqlite-schema--persistence)
- [Testing & Mock Mode](#-testing--mock-mode)
- [Support & Commercial Services](#-support--commercial-services)
- [License](#-license)

---

## 💡 Executive Overview

Modern multi-agent frameworks often introduce sprawling folder structures, dozens of transitive dependencies, obscure abstractions, and unpredictable breaking changes. 

**`mcp-agent-mesh`** delivers an enterprise-grade multi-agent coordination system in a **single, self-contained Python file** (`agent_mesh.py`). It coordinates three specialized AI sub-agents:

1. **🏛️ System Architect**: Analyzes complex engineering requirements, decomposes systems, defines interface schemas, and designs robust component topologies.
2. **💻 Implementation Coder**: Translates architectural specifications into production-ready, typed, idiomatic code with built-in test suites.
3. **🛡️ Security Auditor**: Rigorously analyzes code and architecture for OWASP Top 10 vulnerabilities, calculates a quantitative Security Score (0-100), and outputs hardened patches.
4. **🔄 Auto-Refiner (Optional Loop)**: Feeds auditor findings back to the engineering agent to automatically remediate security flaws in real time.

All interaction prompts, execution latency, structured payloads, and generated deliverables are persistently recorded in a local SQLite database via **SQLAlchemy**.

---

## ⚡ Why `mcp-agent-mesh`?

| Feature | Sprawling Multi-Agent Frameworks | `mcp-agent-mesh` |
|:---|:---|:---|
| **File Count** | 50+ files across nested folders | **1 self-contained file (`agent_mesh.py`)** |
| **Dependencies** | 30+ packages, heavy vector stores | **Just 2: `google-genai` & `sqlalchemy`** |
| **Setup Time** | 15–30 minutes of environment debugging | **Under 60 seconds** |
| **Security Auditing** | None / Addon required | **Native OWASP threat engine & scoring** |
| **Persistence** | Complex cloud / external brokers | **Zero-config local SQLite via SQLAlchemy** |
| **Offline / CI Testing** | Difficult or requires live API keys | **Deterministic mock mode (`--mock`)** |

---

## 📐 System Architecture

```
                                  ┌─────────────────────────────┐
                                  │   USER SPECIFICATION / TASK │
                                  └──────────────┬──────────────┘
                                                 │
                                                 ▼
        ┌──────────────────────────────────────────────────────────────────────────────────┐
        │                          🏛️  SYSTEM ARCHITECT AGENT                              │
        │    Decomposes problem • Produces topological specs • Defines interface schemas   │
        └────────────────────────────────────────┬─────────────────────────────────────────┘
                                                 │ (Architectural Blueprint)
                                                 ▼
        ┌──────────────────────────────────────────────────────────────────────────────────┐
        │                        💻  IMPLEMENTATION CODER AGENT                            │
        │    Synthesizes production code • Type hints • Modular layout • Unit test suites   │
        └────────────────────────────────────────┬─────────────────────────────────────────┘
                                                 │ (Source Code & Tests)
                                                 ▼
        ┌──────────────────────────────────────────────────────────────────────────────────┐
        │                         🛡️  SECURITY AUDITOR AGENT                              │
        │     OWASP Top 10 audit • Vulnerability matrix • Security score (0-100) • Patches │
        └────────────────────────────────────────┬─────────────────────────────────────────┘
                                                 │
                    ┌────────────────────────────┴───────────────────────────┐
                    │ (If score < 85 or CONDITIONAL / FAIL & --refine flag)  │
                    ▼                                                        │
        ┌─────────────────────────────────────────┐                          │
        │       🔄 CODE REFINER AGENT             │                          │
        │   Auto-patches vulnerabilities to v2    │                          │
        └───────────────────┬─────────────────────┘                          │
                            │                                                │
                            └────────────────────┬───────────────────────────┘
                                                 │
                                                 ▼
        ┌──────────────────────────────────────────────────────────────────────────────────┐
        │                        💾  SQLITE STATE PERSISTENCE                              │
        │        Sessions • Steps • Artifacts • Latency Telemetry • Audit Lineage          │
        └────────────────────────────────────────┬─────────────────────────────────────────┘
                                                 │
                                                 ▼
        ┌──────────────────────────────────────────────────────────────────────────────────┐
        │                 📑  UNIFIED MARKDOWN / JSON DELIVERABLES                         │
        └──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 The Autonomous Agent Triad

### 1. 🏛️ System Architect Agent
- **Decomposition**: Breaks user requirements into discrete, testable architectural components.
- **Topological Specification**: Generates ASCII network/component diagrams illustrating data flow.
- **Contract Definition**: Outlines interface protocols, schemas, and invariants.
- **Fault Tolerance**: Defines concurrency models, timeout policies, and state transitions.

### 2. 💻 Implementation Coder Agent
- **Zero Pseudo-Code**: Produces complete, runnable source code without `# TODO` placeholders.
- **Idiomatic & Typed**: Strict type hinting, standard naming conventions, and structured error boundaries.
- **Automated Test Suite**: Every generated service includes a runnable unit test suite (using `unittest` or `pytest`).

### 3. 🛡️ Security Auditor Agent
- **OWASP Threat Modeling**: Evaluates injection risks, broken access controls, secret leaks, and cryptographic hygiene.
- **Quantitative Scoring**: Outputs an authoritative `SECURITY SCORE (0-100)` and `VERDICT (PASS / CONDITIONAL / FAIL)`.
- **Hardened Remediations**: Delivers copy-paste code patches addressing discovered vulnerabilities.

---

## 📦 Prerequisites & Installation

### 1. Requirements
- Python 3.8 or higher
- A Google Gemini API key ([Get a free key here](https://aistudio.google.com/))

### 2. Install Dependencies
```bash
pip install google-genai sqlalchemy
```

### 3. Configure API Key
```bash
# macOS / Linux
export GEMINI_API_KEY="your-gemini-api-key"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-gemini-api-key"

# Windows (CMD)
set GEMINI_API_KEY=your-gemini-api-key
```

---

## 🚀 Quickstart Guide

### Run an Autonomous Multi-Agent Pipeline
Coordinate the full triad to design, implement, and audit a backend service:
```bash
python agent_mesh.py --task "Build a distributed token bucket rate limiter in Python using Redis"
```

### Enable Auto-Refinement & Save to Markdown
Instruct the Security Auditor to automatically trigger a code refiner if issues are detected, saving the full report:
```bash
python agent_mesh.py --task "Implement a secure JWT authentication middleware with refresh tokens" --refine -o jwt_report.md
```

### Run in Offline / Mock Simulation Mode
Verify the full orchestration pipeline, database writes, and artifact rendering without consuming Gemini API quota:
```bash
python agent_mesh.py --task "Design a high-throughput webhook receiver" --mock -o webhook.md
```

### Standalone Security Audit on an Existing File
Point the Security Auditor directly at any local source file to receive an immediate vulnerability analysis:
```bash
python agent_mesh.py --audit-only --code-file server.py -o security_audit.md
```

---

## 🛠️ CLI Command Reference

```
usage: agent_mesh [-h] [-t TASK] [-m MODEL] [-o OUTPUT] [--api-key API_KEY]
                  [--db DB] [--mock] [--refine] [--skip-security]
                  [--audit-only] [--code-file CODE_FILE] [--list-sessions]
                  [--show-session SESSION_ID] [--export-json PATH] [-i] [-v]
                  [--version]
```

| Argument | Description | Default |
|:---|:---|:---|
| `-t`, `--task` | Problem specification or engineering task to orchestrate | `None` |
| `-m`, `--model` | Gemini model (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-pro`) | `gemini-2.5-flash` |
| `-o`, `--output` | Destination file path for compiled Markdown mission report | `None` |
| `--api-key` | Explicit Gemini API Key (overrides `GEMINI_API_KEY` env var) | `None` |
| `--db` | SQLite database file path for state persistence | `agent_mesh.db` |
| `--mock`, `--dry-run` | Run deterministic simulation mode (no API key needed) | `False` |
| `--refine` | Auto-trigger code refiner if security vulnerabilities are found | `False` |
| `--skip-security` | Run only Architect and Coder (omit Security Auditor) | `False` |
| `--audit-only` | Dedicated audit mode on a local file | `False` |
| `--code-file` | Target source code file for `--audit-only` | `None` |
| `--list-sessions` | Display historical execution runs from SQLite database | `False` |
| `--show-session` | Print details and deliverables for a specific session ID | `None` |
| `--export-json` | Export full session telemetry and artifacts to a JSON file | `None` |
| `-i`, `--interactive`| Launch interactive console prompt | `False` |
| `-v`, `--verbose` | Print extended diagnostics and debug logs | `False` |
| `--version` | Display version information | `v1.0.0` |

---

## 💻 Python SDK Programmatic Usage

`mcp-agent-mesh` can be imported as a Python library inside your own applications, CI/CD runners, or custom agents:

```python
from agent_mesh import AgentMesh, MeshConfig

# 1. Configure the mesh engine
config = MeshConfig(
    task="Design an asynchronous event bus with dead-letter queue",
    model="gemini-2.5-flash",
    db_path="agent_mesh.db",
    auto_refine=True,
    output_path="event_bus_deliverable.md",
    verbose=True
)

# 2. Instantiate and execute the coordinator
mesh = AgentMesh(config)
result = mesh.run()

# 3. Inspect results programmatically
print(f"Session ID    : {result.session_id}")
print(f"Security Score: {result.security_score}/100 [{result.security_verdict}]")
print(f"Total Latency : {result.total_latency_ms:.0f}ms")

# Access individual deliverables
print("\n--- Architecture Blueprint ---")
print(result.architecture[:300])

print("\n--- Implementation Code ---")
print(result.implementation[:300])

print("\n--- Security Findings ---")
print(result.security_audit[:300])
```

---

## 💾 SQLite Schema & Persistence

Every run stores structured relational data into SQLite using SQLAlchemy ORM:

```
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│          mesh_sessions          │       │           agent_steps           │
├─────────────────────────────────┤       ├─────────────────────────────────┤
│ session_id (PK, String)         │◄──┐   │ id (PK, Integer)                │
│ task (Text)                     │   └───┤ session_id (FK, String)         │
│ model_name (String)             │       │ agent_role (String)             │
│ status (String)                 │       │ step_number (Integer)           │
│ security_score (Integer)        │       │ prompt_snippet (Text)           │
│ security_verdict (String)       │       │ output_content (Text)           │
│ total_latency_ms (Float)        │       │ latency_ms (Float)              │
│ created_at (DateTime)           │       │ created_at (DateTime)           │
│ completed_at (DateTime)         │       └─────────────────────────────────┘
│ summary (Text)                  │       
└────────────────┬────────────────┘       ┌─────────────────────────────────┐
                 │                        │         mesh_artifacts          │
                 │                        ├─────────────────────────────────┤
                 │                        │ id (PK, Integer)                │
                 └───────────────────────►│ session_id (FK, String)         │
                                          │ artifact_type (String)          │
                                          │ title (String)                  │
                                          │ content (Text)                  │
                                          │ created_at (DateTime)           │
                                          └─────────────────────────────────┘
```

Inspect your stored sessions anytime:
```bash
python agent_mesh.py --list-sessions
python agent_mesh.py --show-session mesh_20261020_054401_3dcbe2
```

---

## 🧪 Testing & Mock Mode

`mcp-agent-mesh` includes an intelligent deterministic mock engine. This enables 100% test coverage in CI/CD environments without requiring API tokens:

```bash
# Verify end-to-end pipeline in simulation mode
python agent_mesh.py --task "Build a Redis key-value store" --mock --refine -o sample.md --export-json sample.json

# Verify standalone security auditor
python agent_mesh.py --audit-only --code-file agent_mesh.py --mock -o self_audit.md
```

---

## ☕ Support & Commercial Services

### ☕ Support Open-Source Development
If `mcp-agent-mesh` saves your team hours of boilerplate or accelerates your prototyping, please consider buying a coffee:

👉 **[Support on Buy Me a Coffee](https://buymeacoffee.com/buildwithjigar)**

---

### 💼 Custom AI & Backend Engineering Services
Are you a tech founder, CTO, or engineering manager looking to build:
- **Custom Autonomous AI Agent Swarms & Tool-Calling Meshes**
- **Model Context Protocol (MCP) Server Infrastructure**
- **Enterprise LLM Workflows & Production RAG Pipelines**
- **High-Throughput Python / Cloud Distributed Backend Systems**

Let's collaborate:
- **Lead Engineer**: Jigar Prajapati
- **LinkedIn**: [linkedin.com/in/jigar48](https://linkedin.com/in/jigar48)
- **Direct Email**: [jigar.prajapati48@gmail.com](mailto:jigar.prajapati48@gmail.com)
- **GitHub**: [@jigar48](https://github.com/jigar48)

---

## 📄 License

This project is licensed under the permissive **MIT License**. See the [LICENSE](LICENSE) file for complete details.

Copyright (c) 2026 Jigar Prajapati.
