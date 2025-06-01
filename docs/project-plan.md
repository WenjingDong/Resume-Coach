# Resume Coach Project Plan

## 1 — Objective

Build an AI‑powered assistant that helps job‑seekers refine their résumés so they pass Applicant Tracking Systems (ATS) and resonate with specific job descriptions. The MVP delivers actionable, evidence‑based feedback and rewritten bullet suggestions in under **10 seconds**.

## 2 — Value Proposition

* **Personalised, LLM‑driven feedback** tuned to role, seniority, and industry.
* **Keyword & gap analysis** against a target JD using semantic search.
* **Instant rewrite suggestions** that preserve the user’s authentic voice while maximising impact.
* **ATS scorecard** highlighting formatting and content issues.
* **One‑click export** to PDF / DOCX with consistent styling.

## 3 — Core Features (MVP)

| # | Capability                                  | Success Metric                         |
| - | ------------------------------------------- | -------------------------------------- |
| 1 | Résumé & JD ingestion (PDF/DOCX/Plain text) | >95 % parse accuracy on sample set     |
| 2 | Embedding & similarity analysis (RAG)       | Top‑10 recall ≥ 90 % for skill matches |
| 3 | Gap report & score (0–100)                  | Correlation ≥ 0.7 with expert ratings  |
| 4 | Bullet rewrite suggestions via LLM          | User acceptance rate ≥ 60 %            |
| 5 | Download polished résumé PDF                | No formatting regressions              |

## 4 — System Architecture (v0.1)

* **Frontend**: React + Tailwind, deployed on Vercel.
* **Backend API**: FastAPI in Docker → AWS ECS Fargate.
* **Vector store**: Pinecone.
* **Embeddings**: OpenAI `text-embedding-3-small` (1536‑d).
* **LLM**: GPT‑4o via OpenAI API; fallback to local Llama 3 8B for cost tests.
* **Orchestration**: LangChain (LCEL).
* **Storage**: S3 (original docs + generated outputs).
* **CI/CD**: GitHub Actions → ECR → ECS blue‑green.
* **Observability**: Prometheus + Grafana; OpenAI token‑usage logging.

## 5 — Eight‑Week Milestones

| Week | Goal                            | Key Tasks                                                 |
| ---- | ------------------------------- | --------------------------------------------------------- |
| 1    | Requirements & design           | Finalise feature list; draw sequence & component diagrams |
| 2    | Data schemas & parsing PoC      | Build PDF ⇄ JSON parser; unit tests                       |
| 3    | Embedding pipeline & vector DB  | Upload 20 sample résumés/JDs; verify similarity search    |
| 4    | Gap analysis & scoring endpoint | Implement `/analyze` in FastAPI; pytest coverage ≥ 80 %   |
| 5    | Front‑end prototype             | File upload; display JSON feedback; CI setup              |
| 6    | LLM rewrite module              | Prompt engineering; safety filters; latency <4 s          |
| 7    | End‑to‑end demo & UX test       | Recruit 3 users; collect SUS & qualitative feedback       |
| 8    | Polish & public launch          | Harden infra; write blog post; deploy demo URL            |

## 6 — Learning Goals

* Practise **ML system design**: retrieval pipelines, vector DB, latency budgets.
* Deepen **prompt engineering** and evaluation for production.
* Solidify **infra skills**: Docker, ECS, CI/CD, monitoring.

## 7 — Evaluation & Metrics

* **Latency**: ≤ 10 s P95 end‑to‑end.
* **Accuracy**: Skill‑gap recall ≥ 90 %.
* **User Satisfaction**: SUS ≥ 70.
* **Cost**: API cost < \$0.05 per full analysis.

