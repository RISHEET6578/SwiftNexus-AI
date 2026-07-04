# SwiftNexus AI🤖📦
# Decoupled Enterprise Support Architecture with Multi-Agent to LCEL Optimization

SwiftNexus AI is a production-grade, decoupled AI customer support application engineered specifically for enterprise logistics and delivery operations. It utilizes Retrieval-Augmented Generation (RAG) to serve zero-hallucination, policy-compliant responses to logistics queries in real time.

## Architecture Overview

The system is engineered using a **decoupled microservices-style architecture** to ensure clear separation of concerns, robust security boundaries, and independent scalability.

```text
+----------------------------+               +----------------------------+
|     Streamlit Frontend     |  REST API     |      FastAPI Backend       |
|  (Hosted on Streamlit Cloud) | ------------> |     (Hosted on Render)     |
+----------------------------+  (HTTP POST)  +----------------------------+
                                                            |
                                             +--------------+--------------+
                                             |                             |
                                             v                             v
                                     +---------------+             +---------------+
                                     |   ChromaDB    |             |  Gemini 1.5   |
                                     | (Vector Store)|             |  Flash-Lite   |
                                     +---------------+             +---------------+
```

**Frontend (UI Layer):** Built with Streamlit, providing a clean, stateful chat interface that handles historical message state tracking completely separate from core backend processing logic.

**Backend (Engine Layer):** Built with FastAPI, securely abstracting private environment keys (GOOGLE_API_KEY), running semantic vector searches, and managing core orchestration.

## Engineering Highlight: The Multi-Agent to LCEL Optimization
### The Problem (The Multi-Agent Bottleneck):
The initial prototype deployed a multi-agent framework utilizing CrewAI (consisting of a Support Agent and a QA Manager Agent). While highly autonomous, the internal conversational loops between agents generated an unexpected cascade of background LLM invocations per single user query. In production, this resulted in:

Immediate RESOURCE_EXHAUSTED (429) rate-limiting exceptions under basic usage tiers.

Unpredictable multi-second execution delays, compromising real-time user UX.

**The Solution (LCEL Refactoring):**
To solve this engineering constraint, the orchestration layer was refactored into a high-performance LangChain Expression Language (LCEL) sequential pipeline. By replacing autonomous agent turn-taking with a targeted, deterministic RAG chain:

1.API Footprint Reduction: Cut background API transactions from 5–8 calls down to exactly 1 call per query.

2.Latency Drop: Reduced end-to-end response times down to sub-second thresholds.

3.Total Reliability: Permanently resolved rate-limit exhaustions while maintaining strict enterprise safety constraints.

**Tech Stack & Pillars:**
1.LLM Engine: Google Gemini 1.5 Flash-Lite (Optimized for fast, low-cost operational tasks).

2.RAG Engine: LangChain Expression Language (LCEL) & ChromaDB (Vector Store).

3.Backend Framework: FastAPI + Uvicorn ASGI Server.

4.Frontend Framework: Streamlit (Session state-tracked).

5.Deployment Infrastructure: GitHub (CI/CD source) + Render Cloud Services (Backend) + Streamlit Community Cloud (Frontend).

# Local Setup & Installation
To spin up this architecture locally on your machine (e.g., inside an Anaconda environment), follow these steps:
**1. Clone and Navigate**
git clone [https://github.com/RISHEET6578/SwiftNexus-AI.git](https://github.com/RISHEET6578/SwiftNexus-AI.git)
cd SwiftNexus-AI
**2. Install Dependencies**
Bash
pip install -r requirements.txt
**3. Environment Configuration**
Create a local .env file in the root directory: GOOGLE_API_KEY="your_actual_gemini_api_key_here"

**4. Fire up the Microservices**
Open two terminal instances to run the decoupled layers concurrently:

**Terminal 1 (Start Backend REST API):**

Bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
**Terminal 2 (Start Frontend Web App):**

Bash
streamlit run app.py

**Enterprise Guardrail Demonstration**
The system utilizes precise contextual system prompting within LCEL to prevent cross-domain prompt injections.

In-Scope Input: "What happens if my package is lost?" * Result: System fetches exact vector insurance rules and crafts a structured resolution protocol.

Out-of-Scope Input: "Can you give me a chocolate chip cookie recipe?"

Result: System elegantly deflects, enforcing business boundaries: "I'm sorry, I can only assist you with logistics, delivery, and corporate shipping policies."

---

## 📬 Contact & Support (Q&A)

Have questions about the architecture, optimization choices, or deployment of **SwiftNexus AI**? Feel free to reach out or connect!

* **GitHub:** [@RISHEET6578](https://github.com/RISHEET6578)
* **LinkedIn:** [Connect me!!](https://www.linkedin.com/in/risheet-sunkari-107429259)
* **Email:** `sunkaririshee2005@gmail.com`

Want to try!! Browse this!!! - https://swiftnexus-ai.streamlit.app/
