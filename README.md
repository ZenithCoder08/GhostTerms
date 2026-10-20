GhostTerms — Autonomous Dark-Pattern & Legal Trap Bounty Agent

Team Name: DeceptiveDefense

Repository: https://github.com/ZenithCoder08/GhostTerms

📌 Executive Summary

Modern consumer platforms heavily deploy manipulative UI/UX patterns (confirm-shaming, roach motels, disguised auto-renewals) and predatory Terms of Service (ToS) clauses (forced arbitration, unilateral amendment rights, silent data distribution).

The Challenge: Conventional web scrapers and static parsers fail against modern client-side Single-Page Applications (SPAs) built with React/Next.js, anti-bot protections, and dynamic, multi-step cancellation dialogs.

The Solution: GhostTerms is an autonomous web-forensics agent engine that crawls, parses, and quantifies deceptive web patterns. Using TinyFish infrastructure for live-web data extraction and cloud browser execution, GhostTerms evaluates services against consumer-protection heuristics to calculate an open, auditable Dark Pattern Index (0–100) and auto-compiles regulatory-ready complaint dossiers.

🚀 Key Features

Real-Time Live Web Discovery: Scans and tracks trending subscription checkouts and updated /terms endpoints.

Context Sanitization: Converts dynamic, JS-heavy SPAs into clean, token-efficient Markdown, preserving LLM context and eliminating hallucination.

Autonomous UX Forensics: Employs goal-directed browser agents to detect hidden cancellation paths, misleading button contrasts, and countdown timer traps.

Semantic Legal Anomaly Detection: Automatically flags predatory fine print, unilateral contract modifications, and non-cancellable recurring billing traps.

Quantifiable Scoring: Generates a standardized 0–100 Dark Pattern Score with severity breakdowns and regulatory export readiness (FTC & EU DSA aligned).

🧠 System Architecture

                  ┌───────────────────────────────┐
                  │    Target Live Web Service    │
                  └──────────────┬────────────────┘
                                 │
                                 ▼
                    [TinyFish Search & Fetch]
                     (Clean DOM & Markdown)
                                 │
            ┌────────────────────┴────────────────────┐
            ▼                                         ▼
   [TinyFish Web Agent]                    [AI/ML Reasoning Core]
(Autonomous Navigation,                   (Multi-Modal Heuristics &
 Modal Interaction & Trace)                Semantic Clause Scoring)
            │                                         │
            └────────────────────┬────────────────────┘
                                 │
                                 ▼
                     [Forensic Audit Engine]
                  - Dark Pattern Index (0-100)
                  - Categorized Violation Log
                  - Regulatory Dossier Package


🐟 Mandatory TinyFish Integration

TinyFish is the foundational infrastructure layer that powers GhostTerms' interaction with the dynamic web:

TinyFish Capability

Project Role & Implementation

Search API

Queries the live web for newly launched SaaS platforms, subscription landing pages, and recently modified legal policy URLs.

Fetch API

Renders client-side SPAs server-side, stripping tracking pixels, cookies, and boilerplate styles into clean Markdown for fast LLM token consumption.

Web Agent & Browser

Controls cloud browser sessions with natural-language instructions to solve cookie dialogs, traverse hidden cancellation menus, detect greyed-out buttons, and record execution traces.

📂 Project Structure

ghostterms-prototype/
├── main.py              # Core GhostTerms auditor & scoring pipeline
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment configuration
├── .gitignore           # Git ignore rules (protects secret keys)
└── README.md            # Comprehensive project documentation


🛠️ Getting Started

Prerequisites

Python 3.9+

Active TinyFish account & API Key

Installation

Clone the repository:

git clone https://github.com/ZenithCoder08/GhostTerms.git
cd GhostTerms


Create and activate a virtual environment:

# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Set up environment variables:

cp .env.example .env


Open .env and insert your TinyFish API key:

TINYFISH_API_KEY=sk-tinyfish-your-key-here


⚡ Running the Prototype

Execute the audit runner:

python main.py


Sample Output Telemetry:

{
  "target_service": "Demonstration Audit Target",
  "dark_pattern_index": 75,
  "risk_tier": "CRITICAL RISK",
  "findings_count": 3,
  "violations": [
    {
      "category": "Roach Motel / Cancellation Friction",
      "severity": "HIGH",
      "matched_evidence": ["written notice required", "cancellation fee"],
      "penalty_points": 25
    },
    {
      "category": "Forced Continuity / Silent Auto-Renew",
      "severity": "HIGH",
      "matched_evidence": ["auto-renew", "without prior notice"],
      "penalty_points": 25
    },
    {
      "category": "Unilateral Rights Alteration",
      "severity": "HIGH",
      "matched_evidence": ["sole discretion to change pricing"],
      "penalty_points": 25
    }
  ],
  "regulatory_complaint_ready": true
}


💼 Business Model & Market Viability

B2B Neo-Banking & Virtual Card APIs: Licensing the scoring engine at $0.02/verification to FinTech platforms to flag subscription traps prior to card authorization.

Enterprise Compliance Sweeps: Retainer subscriptions for consumer advocacy orgs, legal auditors, and regulators.

Consumer Freemium Directory: Free public domain lookup backed by premium instant cancellation execution services.

🗺️ Roadmap & Future Scope

[x] Phase 1: Ingestion pipeline via TinyFish Fetch/Search API.

[x] Phase 2: Heuristic dark-pattern evaluation and 0–100 scoring engine.

[ ] Phase 3: Autonomous multi-step Web Agent cancellation traversal with video logging.

[ ] Phase 4: Chrome extension for real-time checkout warnings.

[ ] Phase 5: Cryptographic audit anchoring on decentralized storage (Arweave/IPFS).

👥 Team: DeceptiveDefense

Lead Architect & Pipeline Systems — Team Lead

Agentic AI & Multi-Modal LLM Core — AI/ML Engineer

Full-Stack & Telemetry Dashboard — Frontend / Backend Lead

📄 License

This project is licensed under the MIT License — see the LICENSE file for details.