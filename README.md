# paralegal_ai_bot

**NOTE** The project is under active development.

## Project Overview
A specialized AI-powered paralegal assistant focused on Indian legal research, leveraging advanced language models and knowledge retrieval technologies to provide comprehensive legal insights.

## Current Architecture
### Core Components
1. **Language Model Base**
   - Built on top of an advanced Large Language Model (LLM)
   - Specialized training in Indian legal terminology and jurisprudence

2. **Retrieval-Augmented Generation (RAG) System**
   - Dynamic information retrieval from multiple legal sources
   - Real-time context-aware legal research capabilities

3. **Data Integration**
   - India Kanoon API integration using Model context protocol
   - Brave search API

### Knowledge Management
1. **Vector Database**
   - Comprehensive legal document repository
   - Includes:
     - Case laws
     - Statutes
     - Judicial precedents
     - Legal commentaries
   - Regularly updated with the latest legal information

2. **Multilingual Support**
   - English and major Indian regional languages
   - Seamless translation of legal documents
   - Preservation of legal nuances during translation

### Proposed Technical Improvements
1. **Machine Learning Models**
   - Continuous learning from new case data
   - Adaptive knowledge base expansion
   - Periodic model retraining

2. **Security and Compliance**
   - End-to-end encryption
   - Strict access controls
   - Compliance with data protection regulations
   - Anonymization of sensitive information

3. **Performance Optimization**
   - Efficient query processing
   - Low-latency information retrieval
   - Scalable cloud infrastructure

## Technologies used

Docker composer - For deployment.
FastApi - For backend.
Crawl4AI - For web crawling and Markdown generation.
Flutter - For frontend.
pipenv - Package manager

## Folder structure

```
paralegal_ai_bot/
├── frontend/
│ └── lib
├── backend/
│ ├── app
│ ├── mcp_1
│ ├── mcp_2
│ ├── .
│ ├── .
│ ├── .
│ └── Pipfile
├── .env
├── .gitignore
├── docker-compose.yaml
├── Dockerfile_api
├── Dockerfile_mcp_1
├── Dockerfile_mcp_2
├── .
├── .
└── README.md
```

## FOR PR's and issues

All PR's are welcome.

1. Use the issue's and pr templates.
2. Please follow the folder structure.
3. Please follow flask8 styling guidelines.
4. No direct commits to main or development branch.
5. Each PR will be tested for integration.

## To Deploy

for local deployment Add all the required fields in to env.example file and rename it to .env
for production deployment use the secret manager provided by your framework.

Looking at the important links section to get api keys.

```
cd paralegal_ai_bot

docker compose up

```

## important links

* [Open AI Docs](https://openrouter.ai/docs/quickstart)
* [India Kanoon](https://api.indiankanoon.org/documentation/)
