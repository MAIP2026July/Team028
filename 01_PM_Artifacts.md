# DESIGN DOCUMENT & PM ARTIFACTS (MARKDOWN FORMAT)

- **Course:** Management of AI Products
- **Assignment:** Experiential Learning Capstone
- **Participants:** Aman Pratap Singh [`2025mb26136`], Aishwarya [`2025mb26138`]
- **Team:** Team028
- **Title:** AI-Assisted Ticket Resolution System (ResolveAI)
- **GitHub Profiles:** [amanpratap28](https://github.com/amanpratap28) | [Aishwarya2809](https://github.com/Aishwarya2809)

---

## Part A: Original Design Document (Converted to Markdown)

### 1. Project Overview
Support teams often spend significant time searching through product documentation and previously resolved client tickets to find solutions for new issues. Even when a similar problem has already been solved, locating the right information can be difficult and time-consuming.

This project proposes an **AI-based Support Assistant** that can search existing documentation and historical support tickets and suggest possible solutions for a new client issue.

### 2. How It Works
The system will use a **Retrieval-Augmented Generation (RAG)** approach:

#### Knowledge Sources:
- Product and technical documentation
- FAQs and troubleshooting guides
- Previously resolved client tickets
- Known issues and their solutions

These sources will be divided into smaller sections and converted into embeddings, which will be stored in a vector database.

#### Issue Retrieval:
When a new client ticket is submitted, the issue will also be converted into an embedding. **Vector similarity search / K-Nearest Neighbours (KNN)** will then be used to find the most relevant documentation and similar historical tickets.

The retrieved information will be passed to the language model as context. The model will use this information to generate a suggested solution rather than relying only on its general knowledge.

### 3. Handling Missing Information
The assistant should not provide a solution when the available information is insufficient.

Instead, it should identify what information is missing and ask the user relevant follow-up questions, such as:
- What error message are you receiving?
- Which application or API version are you using?
- Which API endpoint or feature is affected?
- What steps were performed before the issue occurred?

After receiving the additional information, the system can perform the search again and improve its suggestion.

### 4. Proposed System Flow
`Client Issue` $\rightarrow$ `Query/Embedding` $\rightarrow$ `KNN/Vector Search` $\rightarrow$ `Relevant Documentation & Previous Tickets` $\rightarrow$ `RAG + LLM` $\rightarrow$ `Suggested Solution / Follow-up Questions`

The response can also include the documentation sections or previous ticket references used to generate the suggestion, allowing the support engineer to verify the recommendation.

### 5. Expected Outcome
The goal is to reduce the time spent investigating support issues and make knowledge from previously resolved tickets easier to reuse. The assistant will act as a support tool rather than replacing the support engineer.

The engineer will remain responsible for reviewing the suggested solution and deciding whether it should be provided to the client.

### 6. Key Technologies
`RAG` • `Embeddings` • `Vector Database` • `KNN/Similarity Search` • `Large Language Model (LLM)` • `Document & Ticket Processing`

---

## Part B: Detailed Product Management (PM) Artifacts

### 7. Target User Personas & Jobs-to-be-Done (JTBD)

| Persona | Role & Context | Core Pain Points | Jobs-to-be-Done (JTBD) |
| :--- | :--- | :--- | :--- |
| **Priya (Primary)** — *L1/L2 Support Engineer* | Handles 25–40 client tickets/day across APIs, SDKs, and web apps. | Wastes 15–25 mins per ticket searching Confluence, Zendesk history, and API docs; forgets to ask all clarifying questions in the first reply. | *"When a new client ticket arrives, help me immediately see if we've solved this before, verify the exact doc reference, or tell me what diagnostic questions to ask first."* |
| **Vikram (Secondary)** — *Support Operations Manager* | Manages a 20-person support org; accountable for SLA compliance, MTTR, and CSAT. | High Mean Time to Resolution (MTTR), repeated escalations to L3 engineering for known issues, slow onboarding of new agents. | *"Help my L1 engineers resolve known issues without escalating to L3, while preventing AI hallucinations from reaching enterprise customers."* |
| **Arjun (Stakeholder)** — *Enterprise Client / Developer* | Integrates the company's APIs/products into production systems. | Frustrated by generic copy-paste support replies and multiple rounds of clarifying emails over several days. | *"Give me a fast, accurate technical fix—or ask me all necessary diagnostic questions upfront in a single turn."* |

### 8. Product Goals, North Star Metric & KPIs

- **North Star Metric:** Achieve a **$\ge 35\%$ reduction in Mean Time to Resolution (MTTR)** for L1/L2 technical support tickets within 90 days.

| Metric Category | Specific KPI | Baseline (Current) | Target (MVP) | Measurement Method |
| :--- | :--- | :--- | :--- | :--- |
| **Efficiency** | Average Investigation / Triage Time per Ticket | ~22 mins | **< 8 mins** | Timestamp from ticket open to draft submission |
| **Efficiency** | Back-and-Forth Clarification Turns per Ticket | 3.2 turns | **<= 1.4 turns** | Count of agent-to-client messages before resolution |
| **Adoption** | Engineer Suggestion Acceptance / Edit Rate | N/A | **>= 65%** | % of AI suggestions approved or lightly edited by engineers |
| **Retrieval Quality** | Top-K Citation Relevance (Recall@5) | N/A | **>= 85%** | Engineer thumbs-up/down on cited docs & tickets |
| **AI Safety** | Hallucination / Ungrounded Claim Rate | N/A | **< 2.0%** | Weekly audit of generated drafts vs. retrieved sources |
| **Sufficiency Gate** | Missing-Information Detection Precision | N/A | **>= 85%** | % of follow-up question prompts deemed necessary by L2+ |

### 9. Prioritized Functional Requirements & User Stories (MoSCoW)

| ID | Epic | User Story | Acceptance Criteria | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **US-01** | Knowledge Ingestion | As an Admin, I want to ingest product docs, FAQs, known issues, and historical tickets into a vector store so the AI can search them semantically. | Supports chunking with metadata (`source_type`, `id`, `version`); generates embeddings; stores in vector index. | **Must Have** |
| **US-02** | Semantic Retrieval | As a Support Engineer, I want incoming client tickets automatically converted into embeddings and matched via KNN search against top-K docs and historical tickets. | Returns top-K (configurable, default K=4) chunks with cosine similarity scores in < 2s. | **Must Have** |
| **US-03** | Missing-Info Detection | As a Support Engineer, I want the assistant to detect when a ticket lacks key diagnostic details and suggest specific follow-up questions instead of guessing. | Checks for Error Message, Version, Endpoint/Feature, and Steps; outputs clear follow-up questions when insufficient. | **Must Have** |
| **US-04** | Grounded RAG Solution | As a Support Engineer, I want the LLM to generate a step-by-step resolution strictly grounded in retrieved docs and tickets. | Prompt constrains LLM to retrieved context only; zero fabricated commands or undocumented endpoints. | **Must Have** |
| **US-05** | Verifiable Citations | As a Support Engineer, I want every suggested solution to display the exact documentation sections and historical ticket IDs used. | UI displays citation cards with `Source ID`, `Title`, `Source Type`, `Similarity Score`, and snippet preview. | **Must Have** |
| **US-06** | Multi-Turn Re-Query | As a Support Engineer, I want to append the client's follow-up answers to the original ticket and re-run the search to get an updated solution. | Combines initial issue + follow-up response into an enriched query and transitions from "Follow-up Needed" to "Suggested Solution". | **Must Have** |
| **US-07** | Engineer HITL Review | As a Support Engineer, I want to review, edit, approve, or reject the AI suggestion before anything is sent to the client. | Explicit `Approve & Send`, `Edit Draft`, and `Reject` actions; AI never messages the client directly without engineer sign-off. | **Must Have** |
| **US-08** | Admin Configuration | As a Product Admin, I want to configure similarity thresholds, top-K count, and required diagnostic fields without modifying code. | Externalized configuration via `config.yaml` and runtime settings panel. | **Should Have** |
| **US-09** | Continuous Learning | As a Support Lead, I want newly approved ticket resolutions to be indexed back into the vector database so future tickets benefit immediately. | Approved resolutions can be saved as new `resolved_ticket` records in the knowledge base. | **Should Have** |

### 10. AI Guardrails & Risk Mitigation Matrix

| Risk | Severity | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **LLM Hallucination (Inventing non-existent fixes or API flags)** | High | Medium | Strict system prompt grounding (`temperature=0.1`); hard similarity threshold cutoff; mandatory inline citations; Human-in-the-Loop engineer review before sending. |
| **Stale / Outdated Historical Tickets Overriding New Docs** | Medium | High | Tag chunks with `product_version` and `timestamp`; apply configurable authority weighting (`known_issue > product_doc > faq_guide > resolved_ticket`). |
| **Over-Aggressive Missing-Info Gate (Asking too many questions)** | Medium | Medium | Make required diagnostic slots configurable (`min_required_slots`); allow high-confidence exact error matches to bypass optional slots. |
| **Client PII / Credentials Leaked into Vector DB or LLM** | High | Medium | Regex + NER PII/secret scrubbing pipeline (`API keys`, `emails`, `tokens`) executed prior to embedding generation and storage. |
