 Resume Coach

AI‑powered resume reviewer that surfaces gaps, rewrites bullet points, and exports a recruiter‑ready PDF in seconds.

Built by job‑seekers for job‑seekers — optimise your resume for any job description while keeping your authentic voice.

 Features

| Category | Highlights |
|----------|------------|
| **Keyword & Gap Analysis** | Embedding-based similarity (OpenAI) + rule checks to score alignment with the target JD. |
| **Actionable Feedback** | Concrete suggestions grouped by skill, impact, and formatting. |
| **Smart Bullet Rewrites** | LLM proposes punchier, achievement-oriented bullets you can accept or tweak. |
| **One-Click Export** | Generate polished PDF / DOCX with consistent styling. |

##  Tech Stack

- **Frontend**: React + Tailwind (Vercel)
- **Backend**: FastAPI in Docker (ECS Fargate)
- **Embeddings**: OpenAI `text-embedding-3-small`
- **Vector Store**: PGVector
- **LLM**: Mistral 8B
- **CI/CD**: GitHub Actions → Amazon ECR 🏷️ → ECS Blue-Green
- **Observability**: Prometheus + Grafana, structured logs

##  Quick Start (Local Dev)
Prerequisites: Docker ≥ 25, Python 3.11, make
1. Clone
   
$ git clone https://github.com/WenjingDong/Resume-Coach && cd resume‑coach

2. Bring up dev stack
   
$ make dev   # spins up postgres + backend on http://localhost:8000

3. Run frontend
   
$ cd web && npm install && npm run dev  # http://localhost:3000

4. Run the API
   
$ unicorn backend.main:app --reload

**Run tests**

$ make test   # pytest

**Lint / fmt**

$ pre-commit run --all-files
