# Woyage AI Followup Generator

A FastAPI service that generates follow-up interview questions using OpenAI API.

## Endpoints

### Health Check
`GET /health`

### Generate Followups
`POST /interview/generate-followups`

Request body:
```json
{
  "question": "Tell me about a time you handled conflicting priorities.",
  "answer": "Two urgent client requests collided...",
  "role": "Senior Backend Engineer",
  "interview_type": ["Behavioral interview"]
}
