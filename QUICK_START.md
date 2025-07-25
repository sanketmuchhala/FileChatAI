# Quick Start - Local RAG Chatbot

## If you see "Port 5000 is already in use":

This is normal! The Replit version uses port 5000. For local deployment, use port 8501 instead.

## Simple Commands:

**1. Auto-setup and run (recommended):**
```bash
python setup_and_run.py
```

**2. Manual run with correct port:**
```bash
python -m streamlit run app.py --server.port 8501
```

**3. If port 8501 is also busy, try another port:**
```bash
python -m streamlit run app.py --server.port 8502
```

## Your app will be available at:
- http://localhost:8501 (default)
- http://localhost:8502 (if using alternate port)

## Need API Keys?

Create a `.env` file in the same folder:
```
DEEPSEEK_API_KEY=your_deepseek_key_here
GEMINI_API_KEY=your_gemini_key_here
```

Get keys from:
- DeepSeek: https://platform.deepseek.com
- Gemini: https://ai.google.dev

## Done!
The `setup_and_run.py` script handles everything automatically including port selection.