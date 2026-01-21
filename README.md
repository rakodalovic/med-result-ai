# MedResult AI

A medical laboratory result analysis application that uses AI-powered image
recognition and natural language processing to interpret blood test results and
provide general health advice.

## Overview

MedResult AI is a master's thesis project that combines computer vision and
conversational AI to help users understand their medical laboratory results.
Users can upload images of their blood test results, and the AI chatbot will:

- Extract and interpret the data from the images
- Provide general explanations of what the results mean
- Offer preliminary health advice based on the findings
- Answer questions about specific biomarkers and values

**Important Disclaimer**: This application is designed for educational and
informational purposes only. It does not replace professional medical advice,
diagnosis, or treatment. Always consult with qualified healthcare professionals
regarding your medical results and health conditions.

## Features

- Image upload and processing of blood test results
- Optical character recognition (OCR) for data extraction
- AI-powered interpretation of laboratory values
- Interactive chatbot interface for questions and clarifications
- General health recommendations based on results
- Support for common blood panel formats

## Technology Stack

- Python 3.12+
- Computer Vision and OCR libraries
- AI/ML frameworks for natural language processing
- Web framework for user interface
- Image processing utilities

## Prerequisites

- Python 3.12 or higher
- pip package manager
- Virtual environment support
- Docker and Docker Compose (for database)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MedResult-AI/med-result-ai.git
cd med-result-ai
```

### 2. Create a Virtual Environment

#### On Windows

```bash
python -m venv venv
```

#### On Linux/macOS

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

#### On Windows (Virtual Environment)

```bash
venv\Scripts\activate
```

#### On Linux/macOS (Virtual Environment)

```bash
source venv/bin/activate
```

### 4. Install Dependencies

After activating the virtual environment, install the project with development
and test dependencies:

```bash
pip install -e .[dev,test]
```

This command will install:

- The main application and its core dependencies
- Development tools (linters, formatters, etc.)
- Testing frameworks and utilities

### 5. Set Up the Database

The project uses PostgreSQL for data persistence. A Docker Compose configuration
is provided for easy local development.

#### Start the Database

```bash
docker compose up -d
```

#### Stop the Database

```bash
docker compose down
```

#### Stop and Remove Data

```bash
docker compose down -v
```

#### Check Database Status

```bash
docker compose ps
```

To customize database credentials, copy `.env.example` to `.env` and modify
as needed.

## Configuration

Configuration files and environment variables should be set up before running
the application. Create a `.env` file in the root directory with the following
structure:

```env
API_KEY=your_api_key_here
MODEL_PATH=path/to/model
DEBUG=False
```

## Development

### Setting Up Development Environment

1. Follow the installation steps above
2. Install pre-commit hooks (if configured):

```bash
pre-commit install
```

### Code Style Guidelines

**Line Length:**

- Maximum 80 characters per line for all code
- Maximum 120 characters for some documentation and docstrings

**VS Code Setup:**
Add rulers to your VS Code settings to help maintain line length:

1. Open VS Code settings (JSON): `Ctrl+Shift+P` → "Preferences: Open
   User Settings (JSON)"
2. Add the following configuration:

```json
{
  "editor.rulers": [80, 120]
}
```

This will display vertical lines at columns 80 and 120 as visual guides
while coding.

## Limitations

- The AI provides general information only and should not be used for medical
  diagnosis
- Image quality affects OCR accuracy
- Supports limited blood test formats (see documentation for full list)
- Requires internet connection for AI processing

## Contributing

This is an academic project for a master's thesis. While contributions are not
actively sought, suggestions and feedback are welcome through the issue tracker.

## License

This project is licensed under the MIT License - see the LICENSE file for
details.

## Acknowledgments

- Master's thesis supervisors and academic advisors
- Open-source libraries and frameworks used in this project
- Medical professionals who provided domain expertise

## Contact

For questions or feedback regarding this project, please open an issue on the
GitHub repository or contact the project maintainer.

## Citation

If you use this project in your research or wish to reference it, please cite:

```text
(2026). MedResult AI: AI-Powered Medical Laboratory Result Analysis.
Master's Degree, University of Nis.
```

---

**Developed as part of a Master's thesis in [Your Field]**

**Last Updated**: January 2026
