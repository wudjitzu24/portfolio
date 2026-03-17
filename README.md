# Portfolio Web App

A full-stack web portfolio application built with modern technologies.

## Overview

This project showcases a personal portfolio with a backend API and interactive frontend.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit (Python)

## Project Structure

```
.
├── backend/          # FastAPI application
├── frontend/         # Streamlit application
└── README.md
```

## Getting Started

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend (Streamlit)

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Features

- Display portfolio projects and skills
- Responsive design
- API-driven content management

## Installation

1. Clone the repository
2. Install dependencies for both frontend and backend
3. Configure environment variables as needed
4. Run both applications

## License

MIT
