# MedResult AI

A medical laboratory result analysis application that uses AI-powered image
recognition and natural language processing to interpret blood test results and
provide general health advice.

## Overview

MedResult AI is a master's thesis project that combines computer vision and
conversational AI to help users understand their medical laboratory results.
Users can upload images of their blood test results, and the AI will:

- Extract and interpret data from the images using OCR
- Provide general explanations of what the results mean
- Offer preliminary health advice based on the findings
- Answer follow-up questions about specific biomarkers and values

**Important Disclaimer**: This application is designed for educational and
informational purposes only. It does not replace professional medical advice,
diagnosis, or treatment. Always consult with qualified healthcare professionals
regarding your medical results and health conditions.

## Technology Stack

**Backend**

- Python 3.12+, FastAPI, Uvicorn
- SQLAlchemy 2.0 with PostgreSQL
- Tesseract OCR + OpenCV for image preprocessing
- OpenRouter API (OpenAI-compatible) for LLM inference

**Frontend**

- React 19 + TypeScript + Vite
- Plain CSS with dark-mode-first design

## Prerequisites

- Python 3.12 or higher
- Node.js 18 or higher
- Docker and Docker Compose (for the database)
- Tesseract OCR engine

### Install Tesseract

#### On Ubuntu/Debian

```bash
sudo apt install tesseract-ocr
```

#### On macOS

```bash
brew install tesseract
```

#### On Windows

Download the installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
and add it to your PATH.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MedResult-AI/med-result-ai.git
cd med-result-ai
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
POSTGRES_USER="admin"
POSTGRES_PASSWORD="admin"
POSTGRES_DB="medbot"
POSTGRES_HOST="localhost"
POSTGRES_PORT=5432

OPENROUTER_API_KEY="your-openrouter-api-key"
OPENROUTER_MODEL="google/gemini-2.0-flash-001"
```

Get a free API key at [openrouter.ai](https://openrouter.ai).

### 3. Start the Database

```bash
docker compose up -d
```

### 4. Set Up the Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -e .[dev,test]
```

### 5. Set Up the Frontend

```bash
cd frontend
npm install
```

## Running the Application

Start both servers (from the project root):

**Backend** (default port `8000`):

```bash
cd backend
source venv/bin/activate
uvicorn med_result_ai.main:app --reload
```

**Frontend** (default port `5173`):

```bash
cd frontend
npm run dev
```

## Usage

1. Upload an image of your blood test result (JPEG, PNG, WebP, TIFF, BMP)
2. Wait for the AI to process and analyze the image
3. Read the initial analysis and ask follow-up questions in the chat

## Database Management

```bash
docker compose up -d       # Start
docker compose down        # Stop
docker compose down -v     # Stop and remove all data
docker compose ps          # Check status
```

## VS Code Setup

For Python import resolution, the project includes `.vscode/settings.json`
pointing Pylance to the backend virtual environment. If you use a different
venv path, update `python.defaultInterpreterPath` in that file.

To maintain code style, add rulers to your user settings:

```json
{
  "editor.rulers": [80, 120]
}
```

## Limitations

- The AI provides general information only and must not be used for medical diagnosis
- OCR accuracy depends on image quality and layout
- Requires an internet connection for AI inference

## Contributing

This is an academic project for a master's thesis. Suggestions and feedback
are welcome through the issue tracker.

## License

This project is licensed under the MIT License — see the LICENSE file for details.

## Acknowledgments

- Master's thesis supervisors and academic advisors
- Open-source libraries and frameworks used in this project
- Medical professionals who provided domain expertise

## Citation

If you reference this project, please cite:

```text
MedResult AI (2026): AI-Powered Medical Laboratory Result Analysis.
Master's Degree, Faculty of Electronic Engineering, University of Nis.
```

---
