# paralegal_ai_bot

## Introduction

**NOTE** The project is under active development.

This is a paralegal ai bot build on top of an LLM which specializes in Indian Law.
The current working Idea is to use Retrieval-Augmented Generation to pull information as
required. But eventually there will be a vector database with all the required information
which can then will be updated on a regular basis with current case generation info the most current information.

Currently there is an MCP service connects with India Kanoon API. Please check projects to
look info progress.

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
