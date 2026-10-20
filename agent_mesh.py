"""
# 🕸️ MCP Agent Mesh (`mcp-agent-mesh`)
**Self-Contained Local Multi-Agent Coordination Engine Powered by Google Gemini & SQLAlchemy**

---

## 📌 Executive Overview
`mcp-agent-mesh` is a lightweight, single-file AI multi-agent orchestration utility
designed to coordinate specialized autonomous sub-agents locally. By leveraging
Google's next-generation Gemini models (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-pro`)
alongside structured SQLite state management via SQLAlchemy, `mcp-agent-mesh` eliminates
the brittle overhead of sprawling frameworks.

```
                  ┌─────────────────────────────────────────┐
                  │          USER TASK SPECIFICATION        │
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │     🏛️  SYSTEM ARCHITECT AGENT          │
                  │   Decomposition, Schemas, Interfaces   │
                  └────────────────────┬────────────────────┘
                                       │ (Architecture Spec)
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │    💻  IMPLEMENTATION CODER AGENT       │
                  │    Idiomatic Code, Tests, Edge Cases    │
                  └────────────────────┬────────────────────┘
                                       │ (Source Code & Tests)
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │     🛡️  SECURITY AUDITOR AGENT          │
                  │   OWASP Vulnerability Matrix & Hardening│
                  └────────────────────┬────────────────────┘
                                       │ (Audit Findings)
                         [Optional Auto-Refinement Loop]
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │       💾  SQLITE STATE PERSISTENCE      │
                  │  Sessions, Steps, Artifacts & Audit Log │
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │      📑  UNIFIED MARKDOWN ARTIFACT      │
                  └─────────────────────────────────────────┘
```

---

## 🌟 Core Features
- **Zero-Boilerplate Architecture**: Single, self-contained Python file (`agent_mesh.py`).
- **Autonomous Agent Mesh**:
  1. **System Architect**: Designs system topology, component contracts, and data models.
  2. **Implementation Coder**: Generates complete, production-ready code and test suites.
  3. **Security Auditor**: Conducts OWASP Top 10 threat modeling, computes security scores (0-100),
     and provides hardened remediation diffs.
  4. **Auto-Refinement Loop**: Automatically remediates identified security risks.
- **SQLAlchemy Shared Context**: All agent interactions, prompts, structured payloads, and
  deliverables are persistently tracked in a local SQLite database (`agent_mesh.db`).
- **Mock & Dry-Run Mode**: Full deterministic simulation mode for CI/CD and offline verification.
- **Standalone Security Auditor**: Can audit any external source file via `--audit-only --code-file <path>`.
- **Session History & Export**: Inspect prior runs, view stored artifacts, and export to JSON or Markdown.

---

## 🚀 Quickstart Guide

### 1. Installation
Install the two required dependencies:
```bash
pip install google-genai sqlalchemy
```

### 2. Configure API Key
Set your Google Gemini API key:
```bash
# Linux / macOS
export GEMINI_API_KEY="your-gemini-api-key"

# Windows PowerShell
$env:GEMINI_API_KEY="your-gemini-api-key"

# Windows Command Prompt
set GEMINI_API_KEY=your-gemini-api-key
```

### 3. Run the Mesh
Execute any software engineering or system design task:
```bash
# Standard run
python agent_mesh.py --task "Build a resilient distributed rate limiter with Redis and token bucket"

# Run with security auto-refinement and save output
python agent_mesh.py --task "Build a JWT authentication service in FastAPI" --refine --output jwt_service.md

# Standalone Security Audit on an existing script
python agent_mesh.py --audit-only --code-file server.py --output audit_report.md

# Simulation / Mock Mode (requires no API key)
python agent_mesh.py --task "Implement a secure webhook ingestion endpoint" --mock
```

---

## 💻 Python Library Usage
You can also import and programmatically orchestrate the mesh directly inside your own Python code:

```python
from agent_mesh import AgentMesh, MeshConfig

# Configure the mesh coordinator
config = MeshConfig(
    model="gemini-2.5-flash",
    db_path="agent_mesh.db",
    auto_refine=True,
    verbose=True
)

mesh = AgentMesh(config=config)
session = mesh.run(task="Design and implement a high-throughput event bus in Python")

print(f"Session ID: {session.session_id}")
print(f"Security Score: {session.security_score}/100")
print(session.unified_report)
```

---

## ☕ Support & Commercial Services

### ☕ Support Open Source
If you find `mcp-agent-mesh` valuable, consider buying a coffee to support continued development:
- **Buy Me a Coffee**: [https://buymeacoffee.com/buildwithjigar](https://buymeacoffee.com/buildwithjigar)

### 💼 Custom AI & Backend Engineering Services
Are you a business owner, startup founder, or tech lead looking to build:
- Custom Autonomous AI Agent Swarms & MCP Workflows
- Enterprise LLM Pipelines & Fine-Tuned Systems
- High-Performance Scalable Backend Architectures (Python / Go / Cloud)

Reach out directly to collaborate:
- **Lead Engineer**: Jigar Prajapati
- **LinkedIn**: [https://linkedin.com/in/jigar48](https://linkedin.com/in/jigar48)
- **Email**: `jigar.prajapati48@gmail.com`
- **GitHub**: [https://github.com/jigar48](https://github.com/jigar48)

---
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime
import json
import os
import pathlib
import re
import sys
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

# Ensure UTF-8 output encoding for terminals across platforms (especially Windows)
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Enable ANSI escape sequence processing on Windows
if sys.platform == "win32":
    os.system("")

# ==============================================================================
# Terminal Styling & ANSI Helpers
# ==============================================================================

class Theme:
    """Terminal colors and formatting tokens."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    @classmethod
    def header(cls, text: str) -> str:
        return f"{cls.BOLD}{cls.BRIGHT_CYAN}{text}{cls.RESET}"

    @classmethod
    def success(cls, text: str) -> str:
        return f"{cls.BOLD}{cls.BRIGHT_GREEN}{text}{cls.RESET}"

    @classmethod
    def warning(cls, text: str) -> str:
        return f"{cls.BOLD}{cls.BRIGHT_YELLOW}{text}{cls.RESET}"

    @classmethod
    def error(cls, text: str) -> str:
        return f"{cls.BOLD}{cls.BRIGHT_RED}{text}{cls.RESET}"

    @classmethod
    def info(cls, text: str) -> str:
        return f"{cls.BRIGHT_BLUE}{text}{cls.RESET}"

    @classmethod
    def step(cls, num: str, title: str, subtitle: str = "") -> str:
        sub = f" {Theme.DIM}- {subtitle}{Theme.RESET}" if subtitle else ""
        return f"\n{Theme.BOLD}{Theme.BRIGHT_CYAN}[{num}]{Theme.RESET} {Theme.BOLD}{title}{Theme.RESET}{sub}"


def print_banner() -> None:
    """Displays the branded MCP Agent Mesh ASCII banner."""
    banner = f"""{Theme.BRIGHT_CYAN}
 ███╗   ███╗ ██████╗██████╗      █████╗  ██████╗ ███████╗███╗   ██╗████████╗    ███╗   ███╗███████╗███████╗██╗  ██╗
 ████╗ ████║██╔════╝██╔══██╗    ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝    ████╗ ████║██╔════╝██╔════╝██║  ██║
 ██╔████╔██║██║     ██████╔╝    ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║       ██╔████╔██║█████╗  ███████╗███████║
 ██║╚██╔╝██║██║     ██╔═══╝     ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║       ██║╚██╔╝██║██╔══╝  ╚════██║██╔══██║
 ██║ ╚═╝ ██║╚██████╗██║         ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║       ██║ ╚═╝ ██║███████╗███████║██║  ██║
 ╚═╝     ╚═╝ ╚═════╝╚═╝         ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝       ╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
{Theme.RESET}
 {Theme.BOLD}⚡ MCP AGENT MESH v1.0.0{Theme.RESET} | Autonomous Multi-Agent Coordination Engine
 {Theme.DIM}System Architect 🏛️  ➔  Implementation Coder 💻  ➔  Security Auditor 🛡️  ➔  SQLAlchemy DB 💾{Theme.RESET}
"""
    try:
        print(banner)
    except UnicodeEncodeError:
        print("\n=== MCP AGENT MESH v1.0.0 | Autonomous Multi-Agent Engine ===\n")


def print_footer() -> None:
    """Displays the monetization and commercial consulting CTA box."""
    box = f"""
{Theme.BRIGHT_MAGENTA}╔══════════════════════════════════════════════════════════════════════════════════════════════════╗{Theme.RESET}
{Theme.BRIGHT_MAGENTA}║{Theme.RESET}  {Theme.BOLD}☕ SUPPORT OPEN SOURCE{Theme.RESET}                                                                         {Theme.BRIGHT_MAGENTA}║{Theme.RESET}
{Theme.BRIGHT_MAGENTA}║{Theme.RESET}  Love this tool? Support future releases: {Theme.BRIGHT_YELLOW}https://buymeacoffee.com/buildwithjigar{Theme.RESET}                {Theme.BRIGHT_MAGENTA}║{Theme.RESET}
{Theme.BRIGHT_MAGENTA}║{Theme.RESET}                                                                                                  {Theme.BRIGHT_MAGENTA}║{Theme.RESET}
{Theme.BRIGHT_MAGENTA}║{Theme.RESET}  {Theme.BOLD}💼 CUSTOM AI & BACKEND CONSULTING{Theme.RESET}                                                                 {Theme.BRIGHT_MAGENTA}║{Theme.RESET}
{Theme.BRIGHT_MAGENTA}║{Theme.RESET}  Need custom AI agents, MCP workflows, or scalable backend architecture for your team?            {Theme.BRIGHT_MAGENTA}║{Theme.RESET}
{Theme.BRIGHT_MAGENTA}║{Theme.RESET}  • Connect with {Theme.BOLD}Jigar Prajapati{Theme.RESET} on LinkedIn: {Theme.BRIGHT_CYAN}https://linkedin.com/in/jigar48{Theme.RESET}                         {Theme.BRIGHT_MAGENTA}║{Theme.RESET}
{Theme.BRIGHT_MAGENTA}║{Theme.RESET}  • Direct Inquiries: {Theme.BRIGHT_WHITE}jigar.prajapati48@gmail.com{Theme.RESET}                                                  {Theme.BRIGHT_MAGENTA}║{Theme.RESET}
{Theme.BRIGHT_MAGENTA}╚══════════════════════════════════════════════════════════════════════════════════════════════════╝{Theme.RESET}
"""
    try:
        print(box)
    except UnicodeEncodeError:
        print("\n" + "=" * 80)
        print("Support Open Source: https://buymeacoffee.com/buildwithjigar")
        print("Consulting & Custom AI Agents: Jigar Prajapati (https://linkedin.com/in/jigar48)")
        print("=" * 80 + "\n")


# ==============================================================================
# Database Layer (SQLAlchemy ORM)
# ==============================================================================

def utc_now() -> datetime.datetime:
    """Returns timezone-naive UTC timestamp for SQLAlchemy without deprecation warnings."""
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

try:
    from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, create_engine
    from sqlalchemy.orm import declarative_base, relationship, sessionmaker
    SQLALCH_AVAILABLE = True
except ImportError:
    SQLALCH_AVAILABLE = False
    print(Theme.error("CRITICAL: 'sqlalchemy' is required. Run: pip install sqlalchemy"), file=sys.stderr)

if SQLALCH_AVAILABLE:
    Base = declarative_base()

    class MeshSessionRecord(Base):
        """ORM Model tracking high-level agent mesh execution sessions."""
        __tablename__ = "mesh_sessions"

        session_id = Column(String(64), primary_key=True)
        task = Column(Text, nullable=False)
        model_name = Column(String(64), nullable=False)
        status = Column(String(32), default="RUNNING")
        security_score = Column(Integer, nullable=True)
        security_verdict = Column(String(32), nullable=True)
        created_at = Column(DateTime, default=utc_now)
        completed_at = Column(DateTime, nullable=True)
        total_latency_ms = Column(Float, default=0.0)
        summary = Column(Text, nullable=True)

        steps = relationship("AgentStepRecord", back_populates="session", cascade="all, delete-orphan")
        artifacts = relationship("MeshArtifactRecord", back_populates="session", cascade="all, delete-orphan")

    class AgentStepRecord(Base):
        """ORM Model tracking each agent's individual prompt, output, and execution metrics."""
        __tablename__ = "agent_steps"

        id = Column(Integer, primary_key=True, autoincrement=True)
        session_id = Column(String(64), ForeignKey("mesh_sessions.session_id"), nullable=False)
        agent_role = Column(String(64), nullable=False)
        step_number = Column(Integer, nullable=False)
        prompt_snippet = Column(Text, nullable=True)
        output_content = Column(Text, nullable=False)
        latency_ms = Column(Float, default=0.0)
        created_at = Column(DateTime, default=utc_now)

        session = relationship("MeshSessionRecord", back_populates="steps")

    class MeshArtifactRecord(Base):
        """ORM Model tracking generated deliverables (architecture specs, code, audit reports)."""
        __tablename__ = "mesh_artifacts"

        id = Column(Integer, primary_key=True, autoincrement=True)
        session_id = Column(String(64), ForeignKey("mesh_sessions.session_id"), nullable=False)
        artifact_type = Column(String(32), nullable=False)  # architecture, code, security, report
        title = Column(String(128), nullable=False)
        content = Column(Text, nullable=False)
        created_at = Column(DateTime, default=utc_now)

        session = relationship("MeshSessionRecord", back_populates="artifacts")


class DatabaseManager:
    """Manages SQLite database connections, schema provisioning, and queries."""

    def __init__(self, db_path: str = "agent_mesh.db"):
        self.db_path = db_path
        if not SQLALCH_AVAILABLE:
            self.engine = None
            self.session_factory = None
            return

        # Handle in-memory or file-based sqlite
        if db_path == ":memory:":
            db_url = "sqlite:///:memory:"
        else:
            abs_path = os.path.abspath(db_path)
            db_url = f"sqlite:///{abs_path}"

        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def get_session(self):
        if not self.session_factory:
            raise RuntimeError("SQLAlchemy is not available.")
        return self.session_factory()

    def record_session_start(self, session_id: str, task: str, model_name: str) -> None:
        if not self.session_factory:
            return
        with self.get_session() as s:
            rec = MeshSessionRecord(
                session_id=session_id,
                task=task,
                model_name=model_name,
                status="RUNNING",
                created_at=utc_now(),
            )
            s.add(rec)
            s.commit()

    def record_step(self, session_id: str, agent_role: str, step_num: int,
                    prompt_snippet: str, output: str, latency_ms: float) -> None:
        if not self.session_factory:
            return
        with self.get_session() as s:
            step = AgentStepRecord(
                session_id=session_id,
                agent_role=agent_role,
                step_number=step_num,
                prompt_snippet=prompt_snippet[:1000],
                output_content=output,
                latency_ms=latency_ms,
                created_at=utc_now()
            )
            s.add(step)
            s.commit()

    def record_artifact(self, session_id: str, artifact_type: str, title: str, content: str) -> None:
        if not self.session_factory:
            return
        with self.get_session() as s:
            art = MeshArtifactRecord(
                session_id=session_id,
                artifact_type=artifact_type,
                title=title,
                content=content,
                created_at=utc_now()
            )
            s.add(art)
            s.commit()

    def finalize_session(self, session_id: str, status: str, security_score: Optional[int],
                         security_verdict: Optional[str], summary: str, total_latency_ms: float) -> None:
        if not self.session_factory:
            return
        with self.get_session() as s:
            rec = s.query(MeshSessionRecord).filter_by(session_id=session_id).first()
            if rec:
                rec.status = status
                rec.security_score = security_score
                rec.security_verdict = security_verdict
                rec.summary = summary
                rec.total_latency_ms = total_latency_ms
                rec.completed_at = utc_now()
                s.commit()

    def list_sessions(self, limit: int = 15) -> List[Dict[str, Any]]:
        if not self.session_factory:
            return []
        with self.get_session() as s:
            records = s.query(MeshSessionRecord).order_by(MeshSessionRecord.created_at.desc()).limit(limit).all()
            return [
                {
                    "session_id": r.session_id,
                    "task": r.task[:80] + ("..." if len(r.task) > 80 else ""),
                    "status": r.status,
                    "security_score": r.security_score,
                    "model": r.model_name,
                    "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else "",
                    "total_latency_ms": round(r.total_latency_ms, 2)
                }
                for r in records
            ]

    def get_session_details(self, session_id: str) -> Optional[Dict[str, Any]]:
        if not self.session_factory:
            return None
        with self.get_session() as s:
            r = s.query(MeshSessionRecord).filter_by(session_id=session_id).first()
            if not r:
                return None
            steps = [
                {
                    "role": st.agent_role,
                    "step_number": st.step_number,
                    "latency_ms": st.latency_ms,
                    "content_length": len(st.output_content),
                    "created_at": st.created_at.isoformat() if st.created_at else None,
                }
                for st in r.steps
            ]
            artifacts = [
                {
                    "type": art.artifact_type,
                    "title": art.title,
                    "content": art.content,
                    "created_at": art.created_at.isoformat() if art.created_at else None
                }
                for art in r.artifacts
            ]
            return {
                "session_id": r.session_id,
                "task": r.task,
                "model": r.model_name,
                "status": r.status,
                "security_score": r.security_score,
                "security_verdict": r.security_verdict,
                "total_latency_ms": r.total_latency_ms,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "completed_at": r.completed_at.isoformat() if r.completed_at else None,
                "summary": r.summary,
                "steps": steps,
                "artifacts": artifacts
            }


# ==============================================================================
# Gemini LLM Client Interface & Mock Simulator
# ==============================================================================

class GeminiClient:
    """Wrapper around google-genai SDK with automatic retry, error handling, and mock fallback."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash", is_mock: bool = False):
        self.model = model
        self.is_mock = is_mock
        self.client = None

        if not self.is_mock:
            resolved_key = (
                api_key
                or os.environ.get("GEMINI_API_KEY")
                or os.environ.get("GOOGLE_API_KEY")
            )
            if not resolved_key:
                raise ValueError(
                    "No Gemini API key supplied. Provide --api-key, set GEMINI_API_KEY, "
                    "or specify --mock to run in simulation mode."
                )

            try:
                from google import genai
                self.client = genai.Client(api_key=resolved_key)
            except ImportError:
                raise ImportError(
                    "The 'google-genai' library is required. Install it using:\n"
                    "  pip install google-genai"
                )

    def generate(self, system_instruction: str, user_prompt: str, role: str = "", temperature: float = 0.2) -> Tuple[str, float]:
        """Invokes Gemini or simulated response, returning (content, latency_ms)."""
        start_time = time.time()

        if self.is_mock:
            # Deterministic, realistic mock output tailored to the prompt
            latency = 180.0
            time.sleep(0.15)  # brief simulation delay
            content = self._generate_mock_response(role, system_instruction, user_prompt)
            return content, latency

        # Real Google Gemini API invocation with retry
        from google.genai import types

        max_retries = 3
        backoff = 2.0
        last_err = None

        for attempt in range(1, max_retries + 1):
            try:
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature,
                )
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=user_prompt,
                    config=config,
                )
                latency_ms = (time.time() - start_time) * 1000.0
                return (response.text or "").strip(), latency_ms
            except Exception as e:
                last_err = e
                if attempt < max_retries:
                    time.sleep(backoff)
                    backoff *= 2.0
                else:
                    break

        raise RuntimeError(f"Gemini API invocation failed after {max_retries} attempts: {last_err}")

    def _generate_mock_response(self, role: str, system_instruction: str, user_prompt: str) -> str:
        """Generates rich, realistic mock response based on the active role and prompt."""
        role_key = (role or "").strip().lower()
        sys_key = (system_instruction or "").lower()

        if role_key == "architect" or (not role_key and "architectural blueprint" in sys_key):
            return (
                "### 1. System Architecture Overview\n"
                "The requested solution is structured around an event-driven, decoupled micro-architecture "
                "designed for high resilience, deterministic error recovery, and horizontal scalability.\n\n"
                "#### Architectural Topology\n"
                "```\n"
                " [Client Requests] ──► [API Gateway / Ingestion Layer]\n"
                "                                  │ (Validated Payloads)\n"
                "                                  ▼\n"
                "                       [Core Processing Engine]\n"
                "                                  │\n"
                "                ┌─────────────────┴─────────────────┐\n"
                "                ▼                                   ▼\n"
                "     [Distributed Cache / State]         [Persistent Storage / DB]\n"
                "```\n\n"
                "### 2. Component Specifications & Interfaces\n"
                "- **Ingestion Interface**: Exposes strongly typed, validated endpoint contracts.\n"
                "- **State Manager**: Implements atomic state transitions and concurrency locks.\n"
                "- **Worker Pool**: Asynchronous dispatch mechanism ensuring bounded resource utilization.\n\n"
                "### 3. Implementation Directives for Coder\n"
                "1. Implement strict input validation with boundary checks.\n"
                "2. Provide comprehensive unit tests covering nominal and edge failure modes.\n"
                "3. Ensure all secrets and sensitive identifiers are injected via environment configurations."
            )
        elif role_key == "coder" or (not role_key and "translate the system architect" in sys_key):
            return (
                "```python\n"
                '"""\n'
                'Production-grade implementation based on System Architect specifications.\n'
                '"""\n\n'
                "from __future__ import annotations\n"
                "import os\n"
                "import sys\n"
                "import time\n"
                "import hmac\n"
                "import hashlib\n"
                "import logging\n"
                "from typing import Dict, Any, Optional\n\n"
                "logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')\n"
                "logger = logging.getLogger('mcp_service')\n\n"
                "class ServiceCore:\n"
                "    def __init__(self, secret_key: Optional[str] = None):\n"
                "        self.secret_key = (secret_key or os.environ.get('SERVICE_SECRET', 'dev-default-secret')).encode('utf-8')\n"
                "        self._active_sessions: Dict[str, float] = {}\n\n"
                "    def verify_signature(self, payload: bytes, signature: str) -> bool:\n"
                "        expected = hmac.new(self.secret_key, payload, hashlib.sha256).hexdigest()\n"
                "        return hmac.compare_digest(expected, signature)\n\n"
                "    def process_request(self, request_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:\n"
                "        if not request_id or not isinstance(payload, dict):\n"
                "            raise ValueError('Invalid request envelope: missing request_id or payload')\n"
                "        logger.info(f'Processing request {request_id}')\n"
                "        self._active_sessions[request_id] = time.time()\n"
                "        return {'status': 'SUCCESS', 'request_id': request_id, 'timestamp': time.time()}\n\n"
                "# Unit Test Suite\n"
                "import unittest\n\n"
                "class TestServiceCore(unittest.TestCase):\n"
                "    def setUp(self):\n"
                "        self.service = ServiceCore(secret_key='test-secret-123')\n\n"
                "    def test_signature_verification(self):\n"
                "        payload = b'{\"event\":\"order_created\"}'\n"
                "        valid_sig = hmac.new(b'test-secret-123', payload, hashlib.sha256).hexdigest()\n"
                "        self.assertTrue(self.service.verify_signature(payload, valid_sig))\n"
                "        self.assertFalse(self.service.verify_signature(payload, 'tampered-signature'))\n\n"
                "    def test_process_request_validation(self):\n"
                "        res = self.service.process_request('req-1', {'data': 42})\n"
                "        self.assertEqual(res['status'], 'SUCCESS')\n"
                "        with self.assertRaises(ValueError):\n"
                "            self.service.process_request('', {'data': 42})\n\n"
                "if __name__ == '__main__':\n"
                "    unittest.main()\n"
                "```"
            )
        elif role_key == "auditor" or (not role_key and "penetration tester" in sys_key):
            return (
                "### 🛡️ Security Audit Report & OWASP Threat Analysis\n\n"
                "**OVERALL SECURITY SCORE**: 92 / 100\n"
                "**VERDICT**: PASS\n\n"
                "#### 1. Threat Matrix Assessment\n"
                "- **OWASP A01 (Broken Access Control)**: PASS - State transitions verify session ownership.\n"
                "- **OWASP A02 (Cryptographic Failures)**: PASS - HMAC-SHA256 implemented using constant-time comparison (`hmac.compare_digest`).\n"
                "- **OWASP A03 (Injection Attacks)**: PASS - Strict dictionary schema validation prevents arbitrary structure injection.\n"
                "- **OWASP A05 (Security Misconfiguration)**: LOW RISK - Fallback default secret in dev mode should be blocked in production.\n\n"
                "#### 2. Key Findings & Remediation\n"
                "| Severity | Category | Vulnerability / Issue | Remediation |\n"
                "|:---|:---|:---|:---|\n"
                "| LOW | Secret Mgmt | Hardcoded fallback `'dev-default-secret'` | Raise ValueError if secret key is missing when `ENV=production` |\n"
                "| LOW | Resource Exhaustion | In-memory `_active_sessions` unbounded growth | Enforce TTL expiration or bounded LRU cache |\n\n"
                "#### 3. Hardened Production Patch\n"
                "```python\n"
                "# Enforce strict production secret validation:\n"
                "if os.environ.get('ENV') == 'production' and not os.environ.get('SERVICE_SECRET'):\n"
                "    raise RuntimeError('FATAL: SERVICE_SECRET must be set in production environment!')\n"
                "```"
            )
        elif role_key == "refiner" or (not role_key and "hardening" in sys_key):
            return (
                "```python\n"
                '"""\n'
                'Hardened Production Release (Refined based on Security Audit).\n'
                '"""\n'
                "import os, time, hmac, hashlib, logging\n"
                "from typing import Dict, Any, Optional\n\n"
                "class HardenedServiceCore:\n"
                "    def __init__(self, secret_key: Optional[str] = None):\n"
                "        key = secret_key or os.environ.get('SERVICE_SECRET')\n"
                "        if not key:\n"
                "            if os.environ.get('ENV') == 'production':\n"
                "                raise RuntimeError('SERVICE_SECRET must be configured in production!')\n"
                "            key = 'dev-insecure-fallback-key'\n"
                "        self.secret_key = key.encode('utf-8')\n"
                "        self._active_sessions: Dict[str, float] = {}\n\n"
                "    def verify_signature(self, payload: bytes, signature: str) -> bool:\n"
                "        expected = hmac.new(self.secret_key, payload, hashlib.sha256).hexdigest()\n"
                "        return hmac.compare_digest(expected, signature)\n"
                "```"
            )
        return "Simulated execution output completed successfully."


# ==============================================================================
# Agent Role System Prompts & Logic
# ==============================================================================

ARCHITECT_SYSTEM_PROMPT = """You are the Lead Systems Architect in the MCP Agent Mesh.
Your role is to analyze user tasks, decompose complex engineering requirements, and establish
an authoritative architectural blueprint for implementation engineers.

Your architectural specification must include:
1. Architectural Overview & Component Topology (with ASCII flow diagram).
2. Module Breakdown & Responsibility Matrix.
3. Interface Contracts & Data Schemas (protocols, payload models, endpoints).
4. Concurrency, State Management & Fault-Tolerance Strategy.
5. Specific Implementation Directives & Constraints for the Implementation Coder.

Maintain strict professional engineering standards. Be concise, pragmatic, and explicit.
"""

CODER_SYSTEM_PROMPT = """You are the Senior Principal Software Engineer in the MCP Agent Mesh.
Your role is to translate the System Architect's specification and the original user task
into production-ready, idiomatic, fully functional source code.

Requirements for your output:
1. Provide the complete code implementation in clear code blocks (e.g. ```python ... ```).
2. Write robust error handling, type hints, docstrings, and clean modular structures.
3. Never use pseudo-code or leave '# TODO' placeholders for core business logic.
4. Include a dedicated, runnable unit test suite (e.g. using `unittest` or `pytest`).
5. Include brief instructions on setup, environment variables, and execution.
"""

AUDITOR_SYSTEM_PROMPT = """You are the Security Auditor (Lead Application Security Engineer & Penetration Tester) in the MCP Agent Mesh.
Your role is to perform a rigorous security audit of the provided architecture and implementation code.

Your report must include:
1. Overall Security Score: An integer from 0 to 100. Format strictly as:
   **OVERALL SECURITY SCORE**: <score> / 100
2. Verdict: PASS, CONDITIONAL, or FAIL. Format strictly as:
   **VERDICT**: <verdict>
3. Threat Matrix & OWASP Top 10 Analysis (Injection, Broken Access Control, Cryptography, Secrets, Deserialization, SSRF).
4. Vulnerability Findings Table (Severity: CRITICAL, HIGH, MEDIUM, LOW, Category, Description, Remediation).
5. Hardened Code Patch / Diff demonstrating how to patch the highest risk items.
6. Deployment Security Recommendations.

Be uncompromising in your security evaluation.
"""

REFINER_SYSTEM_PROMPT = """You are the Senior Lead Refactoring & Security Hardening Engineer in the MCP Agent Mesh.
Your role is to take the Implementation Coder's original code and apply the exact fixes, hardening measures,
and vulnerability remediations mandated by the Security Auditor.

Output the complete, unified, hardened source code with all vulnerabilities patched, preserving all original
business logic and unit tests.
"""


# ==============================================================================
# Agent Mesh Coordinator Engine
# ==============================================================================

@dataclasses.dataclass
class MeshConfig:
    """Runtime configuration options for the MCP Agent Mesh."""
    task: str = ""
    model: str = "gemini-2.5-flash"
    db_path: str = "agent_mesh.db"
    api_key: Optional[str] = None
    output_path: Optional[str] = None
    is_mock: bool = False
    auto_refine: bool = False
    skip_security: bool = False
    audit_only: bool = False
    code_file: Optional[str] = None
    verbose: bool = False


@dataclasses.dataclass
class MeshResult:
    """Aggregated output from a completed mesh execution."""
    session_id: str
    task: str
    status: str
    architecture: str
    implementation: str
    security_audit: str
    refined_code: Optional[str]
    security_score: Optional[int]
    security_verdict: Optional[str]
    total_latency_ms: float
    unified_report: str


class AgentMesh:
    """
    Main coordinator for the MCP Agent Mesh.
    Orchestrates the System Architect, Implementation Coder, and Security Auditor,
    persisting all steps and artifacts to SQLite.
    """

    def __init__(self, config: MeshConfig):
        self.config = config
        self.db = DatabaseManager(config.db_path)
        self.llm = GeminiClient(
            api_key=config.api_key,
            model=config.model,
            is_mock=config.is_mock
        )

    def run(self, task: Optional[str] = None) -> MeshResult:
        """Executes the full multi-agent pipeline."""
        active_task = task or self.config.task
        if not active_task:
            raise ValueError("Task cannot be empty. Specify --task or pass a task string.")

        session_id = f"mesh_{utc_now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        start_time = time.time()

        # Record start in database
        self.db.record_session_start(session_id, active_task, self.config.model)

        print(Theme.step("1/3", "🏛️  System Architect Agent", "Analyzing task & designing system topology..."))
        arch_output, arch_latency = self._run_architect(active_task)
        self.db.record_step(session_id, "System Architect", 1, active_task, arch_output, arch_latency)
        self.db.record_artifact(session_id, "architecture", "System Architecture Blueprint", arch_output)
        print(f"    {Theme.success('✓')} Architecture blueprint generated in {arch_latency:.0f}ms")

        print(Theme.step("2/3", "💻 Implementation Coder Agent", "Synthesizing production code & test suites..."))
        code_output, code_latency = self._run_coder(active_task, arch_output)
        self.db.record_step(session_id, "Implementation Coder", 2, arch_output[:400], code_output, code_latency)
        self.db.record_artifact(session_id, "code", "Implementation Source Code & Tests", code_output)
        print(f"    {Theme.success('✓')} Implementation synthesized in {code_latency:.0f}ms")

        audit_output = ""
        security_score = None
        security_verdict = None
        refined_code = None

        if not self.config.skip_security:
            print(Theme.step("3/3", "🛡️  Security Auditor Agent", "Conducting OWASP threat modeling & security audit..."))
            audit_output, audit_latency = self._run_auditor(active_task, arch_output, code_output)
            security_score, security_verdict = self._parse_security_metrics(audit_output)
            self.db.record_step(session_id, "Security Auditor", 3, code_output[:400], audit_output, audit_latency)
            self.db.record_artifact(session_id, "security", "Security Audit & Vulnerability Report", audit_output)

            score_badge = f"{security_score}/100" if security_score is not None else "N/A"
            verdict_badge = security_verdict or "REVIEWED"
            print(f"    {Theme.success('✓')} Security audit completed in {audit_latency:.0f}ms | Score: {Theme.BOLD}{score_badge}{Theme.RESET} [{verdict_badge}]")

            # Check for auto-refinement trigger
            should_refine = self.config.auto_refine and (
                (security_score is not None and security_score < 85)
                or (security_verdict in ["CONDITIONAL", "FAIL"])
            )

            if should_refine:
                print(Theme.step("4/4", "🔄 Code Refiner Agent", "Auto-patching vulnerabilities from audit findings..."))
                refined_code, refiner_latency = self._run_refiner(code_output, audit_output)
                self.db.record_step(session_id, "Code Refiner", 4, audit_output[:400], refined_code, refiner_latency)
                self.db.record_artifact(session_id, "refined_code", "Hardened Production Code", refined_code)
                print(f"    {Theme.success('✓')} Hardened code revision generated in {refiner_latency:.0f}ms")

        total_latency = (time.time() - start_time) * 1000.0

        # Build unified markdown report
        unified_report = self._build_unified_report(
            session_id=session_id,
            task=active_task,
            architecture=arch_output,
            implementation=code_output,
            security_audit=audit_output,
            refined_code=refined_code,
            security_score=security_score,
            security_verdict=security_verdict,
            total_latency_ms=total_latency
        )

        # Record report artifact and finalize session in DB
        self.db.record_artifact(session_id, "report", "Unified Mission Report", unified_report)
        self.db.finalize_session(
            session_id=session_id,
            status="COMPLETED",
            security_score=security_score,
            security_verdict=security_verdict,
            summary=f"Task: {active_task[:100]} | Model: {self.config.model}",
            total_latency_ms=total_latency
        )

        # Write output file if requested
        if self.config.output_path:
            out_file = pathlib.Path(self.config.output_path)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(unified_report, encoding="utf-8")
            print(f"\n{Theme.success('💾')} Report saved to: {Theme.BOLD}{out_file.resolve()}{Theme.RESET}")

        result = MeshResult(
            session_id=session_id,
            task=active_task,
            status="COMPLETED",
            architecture=arch_output,
            implementation=code_output,
            security_audit=audit_output,
            refined_code=refined_code,
            security_score=security_score,
            security_verdict=security_verdict,
            total_latency_ms=total_latency,
            unified_report=unified_report
        )
        return result

    def run_audit_only(self, code_content: str, file_name: str = "target_code") -> MeshResult:
        """Runs the standalone security auditor on an existing code file."""
        session_id = f"audit_{utc_now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        task = f"Perform dedicated security audit on file: {file_name}"
        start_time = time.time()

        self.db.record_session_start(session_id, task, self.config.model)

        print(Theme.step("1/1", "🛡️  Security Auditor Agent", f"Auditing file {file_name} for vulnerabilities..."))
        prompt = f"Target File: {file_name}\n\nSource Code:\n```\n{code_content}\n```"
        audit_output, audit_latency = self.llm.generate(AUDITOR_SYSTEM_PROMPT, prompt, role="auditor")
        security_score, security_verdict = self._parse_security_metrics(audit_output)

        self.db.record_step(session_id, "Security Auditor", 1, prompt[:400], audit_output, audit_latency)
        self.db.record_artifact(session_id, "security", f"Security Audit for {file_name}", audit_output)

        total_latency = (time.time() - start_time) * 1000.0

        score_badge = f"{security_score}/100" if security_score is not None else "N/A"
        verdict_badge = security_verdict or "REVIEWED"
        print(f"    {Theme.success('✓')} Security audit completed in {audit_latency:.0f}ms | Score: {Theme.BOLD}{score_badge}{Theme.RESET} [{verdict_badge}]")

        unified_report = self._build_audit_only_report(
            session_id=session_id,
            file_name=file_name,
            code_content=code_content,
            audit_output=audit_output,
            security_score=security_score,
            security_verdict=security_verdict,
            total_latency_ms=total_latency
        )

        self.db.record_artifact(session_id, "report", f"Audit Report: {file_name}", unified_report)
        self.db.finalize_session(
            session_id=session_id,
            status="COMPLETED",
            security_score=security_score,
            security_verdict=security_verdict,
            summary=f"Audit: {file_name} | Score: {security_score}",
            total_latency_ms=total_latency
        )

        if self.config.output_path:
            out_file = pathlib.Path(self.config.output_path)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(unified_report, encoding="utf-8")
            print(f"\n{Theme.success('💾')} Audit report saved to: {Theme.BOLD}{out_file.resolve()}{Theme.RESET}")

        return MeshResult(
            session_id=session_id,
            task=task,
            status="COMPLETED",
            architecture="",
            implementation=code_content,
            security_audit=audit_output,
            refined_code=None,
            security_score=security_score,
            security_verdict=security_verdict,
            total_latency_ms=total_latency,
            unified_report=unified_report
        )

    # --------------------------------------------------------------------------
    # Sub-Agent Invocation Helpers
    # --------------------------------------------------------------------------

    def _run_architect(self, task: str) -> Tuple[str, float]:
        user_prompt = f"User Engineering Task:\n{task}\n\nProduce the comprehensive System Architecture Blueprint."
        return self.llm.generate(ARCHITECT_SYSTEM_PROMPT, user_prompt, role="architect")

    def _run_coder(self, task: str, architecture: str) -> Tuple[str, float]:
        user_prompt = (
            f"Original Task:\n{task}\n\n"
            f"System Architecture Blueprint:\n{architecture}\n\n"
            "Synthesize the complete, production-ready implementation code and test suite."
        )
        return self.llm.generate(CODER_SYSTEM_PROMPT, user_prompt, role="coder")

    def _run_auditor(self, task: str, architecture: str, code: str) -> Tuple[str, float]:
        user_prompt = (
            f"Original Task:\n{task}\n\n"
            f"Architectural Context:\n{architecture[:1500]}\n\n"
            f"Implementation Code to Audit:\n{code}\n\n"
            "Conduct the formal security audit, compute the security score, and list findings."
        )
        return self.llm.generate(AUDITOR_SYSTEM_PROMPT, user_prompt, role="auditor")

    def _run_refiner(self, code: str, audit: str) -> Tuple[str, float]:
        user_prompt = (
            f"Original Implementation Code:\n{code}\n\n"
            f"Security Audit & Remediation Directives:\n{audit}\n\n"
            "Output the updated, hardened, production-ready code with all security flaws patched."
        )
        return self.llm.generate(REFINER_SYSTEM_PROMPT, user_prompt, role="refiner")

    # --------------------------------------------------------------------------
    # Parsing & Report Compilation
    # --------------------------------------------------------------------------

    def _parse_security_metrics(self, audit_text: str) -> Tuple[Optional[int], Optional[str]]:
        score = None
        verdict = None

        # Extract Security Score: **OVERALL SECURITY SCORE**: 92 / 100 or Security Score: 85
        score_match = re.search(r"SECURITY\s+SCORE\*?\*?:\s*(\d{1,3})", audit_text, re.IGNORECASE)
        if score_match:
            try:
                parsed = int(score_match.group(1))
                if 0 <= parsed <= 100:
                    score = parsed
            except ValueError:
                pass

        # Extract Verdict: PASS, CONDITIONAL, FAIL
        verdict_match = re.search(r"VERDICT\*?\*?:\s*(PASS|CONDITIONAL|FAIL)", audit_text, re.IGNORECASE)
        if verdict_match:
            verdict = verdict_match.group(1).upper()

        return score, verdict

    def _build_unified_report(self, session_id: str, task: str, architecture: str,
                              implementation: str, security_audit: str, refined_code: Optional[str],
                              security_score: Optional[int], security_verdict: Optional[str],
                              total_latency_ms: float) -> str:
        score_badge = f"{security_score}/100" if security_score is not None else "N/A"
        verdict_badge = security_verdict or "NOT REVIEWED"
        timestamp = utc_now().strftime("%Y-%m-%d %H:%M:%S UTC")

        refined_section = ""
        if refined_code:
            refined_section = f"""
## 4. 🔄 Auto-Hardened Implementation Revision
*Synthesized by Code Refiner to patch vulnerabilities identified during security audit.*

{refined_code}
"""

        report = f"""# 🕸️ MCP Agent Mesh: Mission Execution Report
**Session ID:** `{session_id}`  
**Generated At:** `{timestamp}`  
**Model:** `{self.config.model}` | **Total Latency:** `{total_latency_ms:.0f}ms`  
**Security Score:** `{score_badge}` | **Security Verdict:** `{verdict_badge}`

---

## 🎯 Task Specification
> {task}

---

## 1. 🏛️ System Architecture Blueprint
*Authored by System Architect Agent*

{architecture}

---

## 2. 💻 Implementation Code & Test Suite
*Authored by Implementation Coder Agent*

{implementation}

---

## 3. 🛡️ Security Audit & Threat Assessment
*Authored by Security Auditor Agent*

{security_audit}

---
{refined_section}
---

## ☕ Support & Commercial Services

### ☕ Support Open Source
If `mcp-agent-mesh` accelerated your workflow, consider supporting development:
- **Buy Me a Coffee**: [https://buymeacoffee.com/buildwithjigar](https://buymeacoffee.com/buildwithjigar)

### 💼 Custom AI & Backend Engineering Services
Need custom AI agent swarms, MCP integrations, or high-performance backend systems built for your company?
- **Lead Engineer**: Jigar Prajapati
- **LinkedIn**: [https://linkedin.com/in/jigar48](https://linkedin.com/in/jigar48)
- **Email**: `jigar.prajapati48@gmail.com`
- **GitHub**: [https://github.com/jigar48](https://github.com/jigar48)
"""
        return report.strip()

    def _build_audit_only_report(self, session_id: str, file_name: str, code_content: str,
                                audit_output: str, security_score: Optional[int],
                                security_verdict: Optional[str], total_latency_ms: float) -> str:
        score_badge = f"{security_score}/100" if security_score is not None else "N/A"
        verdict_badge = security_verdict or "REVIEWED"
        timestamp = utc_now().strftime("%Y-%m-%d %H:%M:%S UTC")

        report = f"""# 🛡️ MCP Agent Mesh: Standalone Security Audit Report
**Session ID:** `{session_id}`  
**Target File:** `{file_name}`  
**Audit Timestamp:** `{timestamp}`  
**Model:** `{self.config.model}` | **Audit Latency:** `{total_latency_ms:.0f}ms`  
**Security Score:** `{score_badge}` | **Verdict:** `{verdict_badge}`

---

## 📋 Security Assessment & Threat Model
{audit_output}

---

## 📄 Audited Source Code
```
{code_content}
```

---

## ☕ Support & Commercial Services
- **Buy Me a Coffee**: [https://buymeacoffee.com/buildwithjigar](https://buymeacoffee.com/buildwithjigar)
- **Custom Security & Agent Consulting**: [https://linkedin.com/in/jigar48](https://linkedin.com/in/jigar48)
- **Contact**: `jigar.prajapati48@gmail.com`
"""
        return report.strip()


# ==============================================================================
# CLI Entrypoint & Argument Parsing
# ==============================================================================

def build_cli_parser() -> argparse.ArgumentParser:
    """Configures the command-line interface arguments."""
    parser = argparse.ArgumentParser(
        prog="agent_mesh",
        description="mcp-agent-mesh: Autonomous Multi-Agent Coordinator powered by Google Gemini & SQLAlchemy.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Autonomous pipeline execution
  python agent_mesh.py --task "Build a resilient distributed cache with TTL and Redis backend"

  # Run with security auto-refinement and save report to Markdown
  python agent_mesh.py --task "Implement a secure JWT auth flow in FastAPI" --refine -o jwt_flow.md

  # Simulation / Mock Mode (requires no API key)
  python agent_mesh.py --task "Design a webhook receiver" --mock

  # Dedicated security audit of a local file
  python agent_mesh.py --audit-only --code-file server.py -o server_audit.md

  # List prior execution sessions
  python agent_mesh.py --list-sessions

  # Inspect a past session report
  python agent_mesh.py --show-session mesh_20261020_123456_abcdef
        """
    )

    # Core execution arguments
    parser.add_argument("-t", "--task", type=str, help="Engineering task or problem description for the agent mesh.")
    parser.add_argument("-m", "--model", type=str, default="gemini-2.5-flash", help="Gemini model name (default: gemini-2.5-flash).")
    parser.add_argument("-o", "--output", type=str, help="Destination filepath to save the compiled Markdown report.")
    parser.add_argument("--api-key", type=str, help="Gemini API Key (overrides GEMINI_API_KEY env variable).")
    parser.add_argument("--db", type=str, default="agent_mesh.db", help="SQLite database path for mesh state persistence (default: agent_mesh.db).")

    # Workflow modifiers
    parser.add_argument("--mock", "--dry-run", dest="is_mock", action="store_true", help="Run with deterministic simulation agent responses (no API key required).")
    parser.add_argument("--refine", action="store_true", help="Automatically trigger code refiner if security auditor identifies vulnerabilities.")
    parser.add_argument("--skip-security", action="store_true", help="Execute Architect and Coder while skipping the Security Auditor.")

    # Dedicated audit mode
    parser.add_argument("--audit-only", action="store_true", help="Run in standalone Security Auditor mode on a local file.")
    parser.add_argument("--code-file", type=str, help="Path to code file to audit (used with --audit-only).")

    # Persistence & History utilities
    parser.add_argument("--list-sessions", action="store_true", help="List recent execution sessions stored in SQLite.")
    parser.add_argument("--show-session", type=str, metavar="SESSION_ID", help="Print details and report for a specific session ID.")
    parser.add_argument("--export-json", type=str, metavar="PATH", help="Export full session history and artifacts to a JSON file.")

    # Interactive and diagnostics
    parser.add_argument("-i", "--interactive", action="store_true", help="Launch interactive prompt mode.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose diagnostics.")
    parser.add_argument("--version", action="version", version="mcp-agent-mesh v1.0.0")

    return parser


def handle_list_sessions(db: DatabaseManager) -> None:
    """Prints recent sessions in a formatted table."""
    sessions = db.list_sessions(limit=20)
    if not sessions:
        print(f"{Theme.warning('ℹ')} No execution sessions found in database `{db.db_path}`.")
        return

    print(f"\n{Theme.header('Recent Mesh Sessions (Database: ' + db.db_path + ')')}")
    print("─" * 96)
    print(f"{'Session ID':<34} {'Created':<20} {'Status':<10} {'Score':<8} {'Model':<18}")
    print("─" * 96)
    for s in sessions:
        score_str = str(s['security_score']) if s['security_score'] is not None else "-"
        print(f"{s['session_id']:<34} {s['created_at']:<20} {s['status']:<10} {score_str:<8} {s['model']:<18}")
    print("─" * 96)


def handle_show_session(db: DatabaseManager, session_id: str) -> None:
    """Displays stored artifacts and details for a given session."""
    details = db.get_session_details(session_id)
    if not details:
        print(f"{Theme.error('Error:')} Session ID `{session_id}` not found.")
        return

    print(f"\n{Theme.header('Session Details:')} {Theme.BOLD}{details['session_id']}{Theme.RESET}")
    print(f"  Task: {details['task']}")
    print(f"  Model: {details['model']} | Status: {details['status']} | Security Score: {details['security_score']}")
    print(f"  Created: {details['created_at']} | Latency: {details['total_latency_ms']:.0f}ms")

    report_artifact = next((a for a in details["artifacts"] if a["type"] == "report"), None)
    if report_artifact:
        print("\n" + "=" * 80)
        print(report_artifact["content"])
        print("=" * 80)
    else:
        print(f"\n{Theme.info('Artifacts in session:')}")
        for a in details["artifacts"]:
            print(f"  - [{a['type']}] {a['title']} ({len(a['content'])} characters)")


def handle_export_json(db: DatabaseManager, session_id: str, export_path: str) -> None:
    """Exports session details to a JSON file."""
    details = db.get_session_details(session_id)
    if not details:
        print(f"{Theme.error('Error:')} Session `{session_id}` not found.")
        return

    path = pathlib.Path(export_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(details, indent=2), encoding="utf-8")
    print(f"{Theme.success('✓')} Exported session data to: {path.resolve()}")


def main() -> int:
    """CLI execution entrypoint."""
    parser = build_cli_parser()
    args = parser.parse_args()

    print_banner()

    # Session inspection subcommands
    db = DatabaseManager(args.db)

    if args.list_sessions:
        handle_list_sessions(db)
        print_footer()
        return 0

    if args.show_session:
        handle_show_session(db, args.show_session)
        print_footer()
        return 0

    # Standalone audit mode
    if args.audit_only:
        if not args.code_file:
            print(Theme.error("Error: --audit-only requires --code-file <path>"), file=sys.stderr)
            return 1

        file_path = pathlib.Path(args.code_file)
        if not file_path.exists():
            print(Theme.error(f"Error: Target file not found: {args.code_file}"), file=sys.stderr)
            return 1

        code_content = file_path.read_text(encoding="utf-8")

        config = MeshConfig(
            model=args.model,
            db_path=args.db,
            api_key=args.api_key,
            output_path=args.output,
            is_mock=args.is_mock,
            verbose=args.verbose
        )

        mesh = AgentMesh(config)
        mesh.run_audit_only(code_content=code_content, file_name=file_path.name)
        print_footer()
        return 0

    # Standard task execution or interactive mode
    task = args.task
    if args.interactive and not task:
        print(f"{Theme.header('Interactive Mode')} - Enter your engineering task below:")
        try:
            task = input(f"{Theme.BOLD}Task > {Theme.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            return 0

    if not task:
        parser.print_help()
        print_footer()
        return 1

    config = MeshConfig(
        task=task,
        model=args.model,
        db_path=args.db,
        api_key=args.api_key,
        output_path=args.output,
        is_mock=args.is_mock,
        auto_refine=args.refine,
        skip_security=args.skip_security,
        verbose=args.verbose
    )

    try:
        mesh = AgentMesh(config)
        result = mesh.run()

        # If no specific output file was saved, render summary snippet
        if not args.output:
            print(f"\n{Theme.header('═══════════════════════ Mission Execution Summary ═══════════════════════')}")
            print(f"Session ID : {result.session_id}")
            print(f"Status     : {result.status}")
            print(f"Security   : {result.security_score or 'N/A'}/100 [{result.security_verdict or 'N/A'}]")
            print(f"Latency    : {result.total_latency_ms:.0f}ms")
            print(f"Database   : {args.db}")
            print(f"{Theme.DIM}Tip: Pass -o <report.md> to export the complete report and source code.{Theme.RESET}")

        if args.export_json:
            handle_export_json(db, result.session_id, args.export_json)

    except Exception as e:
        print(f"\n{Theme.error('FATAL EXECUTION ERROR:')} {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        print_footer()
        return 1

    print_footer()
    return 0


if __name__ == "__main__":
    sys.exit(main())
