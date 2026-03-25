# Invoice Extractor

An AI-powered invoice data extraction tool built with FastAPI and Angular. Upload a PDF invoice and get structured data extracted instantly using Claude's vision API.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Python |
| Frontend | Angular 21 + TypeScript |
| AI | Anthropic Claude Sonnet (Vision) |
| Server | Uvicorn (ASGI) |

## Features

- Upload PDF invoices via drag-and-drop or file picker
- Extracts key fields: vendor, invoice number, date, due date, line items, subtotal, tax, total
- Clean results page with structured display
- Fully stateless — no database required

## Project Structure

```
invoice-extractor/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── config.py        # Environment config
│   │   ├── models/          # Pydantic data models
│   │   ├── routers/         # API route handlers
│   │   └── services/        # Claude API integration
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   └── app/
    │       ├── components/  # Shared components (header)
    │       ├── pages/       # Upload and Result pages
    │       ├── services/    # HTTP service layer
    │       └── models/      # TypeScript interfaces
    ├── proxy.conf.json      # Dev proxy to backend
    └── package.json
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+ and npm
- Anthropic API key ([get one here](https://console.anthropic.com/))

### 1. Clone the repo

```bash
git clone https://github.com/VishalSonone/invoice-extractor.git
cd invoice-extractor
```

### 2. Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your API key:

```bash
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY=sk-ant-...
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`

### 3. Frontend setup

```bash
cd frontend
npm install
ng serve
```

Frontend runs at `http://localhost:4200`

### 4. Open the app

Navigate to `http://localhost:4200` — the frontend proxies all `/api` requests to the backend automatically.

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload` | Upload PDF, returns extracted invoice data |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
