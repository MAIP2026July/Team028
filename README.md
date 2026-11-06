================================================================================
AI-ASSISTED TICKET RESOLUTION SYSTEM (ResolveAI)
================================================================================
Course     : Management of AI Products
Assignment : Experiential Learning Capstone
Team       : Team028
================================================================================

1. TEAM MEMBER DETAILS
--------------------------------------------------------------------------------
Name              : Aman Pratap Singh
Student / Roll ID : 2025mb26136
Role              : Product Manager & RAG Architecture Lead
GitHub ID         : @amanpratap28
GitHub Profile    : https://github.com/amanpratap28

Name              : Aishwarya
Student / Roll ID : 2025mb26138
Role              : Product Manager & AI Evaluation / Workflow Lead
GitHub ID         : @Aishwarya2809
GitHub Profile    : https://github.com/Aishwarya2809
--------------------------------------------------------------------------------


2. PROJECT OVERVIEW
--------------------------------------------------------------------------------
Support engineering teams spend 40-60% of their investigation time searching
across fragmented product documentation, troubleshooting guides, and historical
resolved tickets to diagnose incoming client issues. Even when a nearly
identical problem has already been solved in the past, locating the right
context is slow and error-prone.

ResolveAI (AI-Assisted Ticket Resolution System) is a Human-in-the-Loop (HITL)
Retrieval-Augmented Generation (RAG) support assistant designed to:

  1) Unify Knowledge Sources:
     Ingest and chunk product documentation, FAQs, troubleshooting guides,
     known issues, and previously resolved client tickets into vector
     embeddings.

  2) Retrieve Relevant Context via KNN / Vector Search:
     Match incoming client issues against historical tickets and official
     documentation using semantic similarity.

  3) Detect Missing Information Proactively:
     Refuse to guess or hallucinate when a ticket lacks critical diagnostic
     details (error message, API/application version, affected endpoint,
     reproduction steps) and instead generate targeted follow-up questions.

  4) Generate Grounded, Citation-Backed Solutions:
     Provide support engineers with a draft resolution alongside verifiable
     references to the exact documentation sections and historical ticket IDs.

  5) Keep the Support Engineer in Control:
     Act as a decision-support co-pilot where the engineer reviews, edits, and
     approves the final response before sending it to the client.


3. REPOSITORY & DELIVERABLES STRUCTURE
--------------------------------------------------------------------------------
ai-ticket-resolution-system/
|-- README.txt                                 (Deliverable 5: Team details & GitHub IDs)
|-- README.md                                  (Markdown version of README)
|-- 01_PM_Artifacts.docx / .md                 (Deliverable 1: PM Artifacts & PRD)
|-- 02_AI_Self_Evaluation.docx / .md           (Deliverable 2: AI Self-Evaluation Report)
|-- 03_MVP_Monetization_Roadmap.docx / .md     (Deliverable 3: MVP & Monetization Roadmap)
|-- 04_Workflow_Swimlane.docx / .md            (Deliverable 4: Initial & Updated Swimlanes)
|-- Team028_Complete_Assignment_1_to_4.docx    (Combined Word file for Deliverables 1-4)
|-- docs/
|   |-- workflow_initial.puml                  (Initial Swimlane PlantUML source)
|   `-- workflow_updated.puml                  (Updated Swimlane PlantUML source)
`-- product/                                   (Deliverable 2: Working AI Product Prototype)
    |-- config.yaml                            (Externalized configurable parameters)
    |-- knowledge_base.json                    (Seeded vector store chunks)
    |-- app.py                                 (Python RAG + Sufficiency Gate engine)
    `-- index.html                             (Interactive Browser Support Co-Pilot UI)


4. QUICK START: RUNNING THE BUILT PRODUCT (DELIVERABLE 2)
--------------------------------------------------------------------------------
Option A: Interactive Web Console (Zero Setup)
  Open product/index.html directly in any web browser to:
  - Test complete tickets (KNN retrieval + grounded RAG fix + citations).
  - Test incomplete tickets (triggers Missing-Info Gate & follow-up questions).
  - Adjust configurable thresholds live in the right-hand control panel.

Option B: Python CLI Engine
  Run the automated 3-scenario demo:
    python3 product/app.py --demo

  Or evaluate a custom ticket:
    python3 product/app.py --ticket "Getting 401 token expired error on /v2/payments/charge in SDK v2.4 after rotating keys"
================================================================================
