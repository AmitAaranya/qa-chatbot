# QA Chatbot

[![QA App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://app-chatbot-amit.streamlit.app/)

A question-answering chatbot powered by Google's Gemini LLM and Streamlit. The application allows users to upload FAQ data and get accurate answers based on the provided context.

## Technologies Used

- **Python** (>=3.13)
- **Streamlit** - Web application framework
- **Google Gemini** - Large Language Model for natural language processing
- **ChromaDB** - Vector database for efficient similarity search
- **Embedding Model** - For text embeddings chunks, model:  `all-MiniLM-L6-v2` (default for ChromaDB)
- **Pandas** - For data manipulation and CSV processing

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AmitAaranya/qa-chatbot.git
   cd qa-chatbot
   ```

2. Install uv (if not already installed):
   ```bash
   pip install uv
   ```

3. Create and activate virtual environment using uv:
   ```bash
   uv venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On Unix/MacOS
   ```

4. Install dependencies using uv:
   ```bash
   uv sync
   ```

5. Create `.env` file
6. Configure your Google API key for Gemini LLM with `GOOGLE_GEMINI_API_KEY`

## Running the Application

Run the Streamlit app using:
```bash
streamlit run streamlit_run.py
```

The application will be available at http://localhost:8501

## User Guide

### Uploading FAQ Data
1. Prepare your FAQ data in CSV format with two required columns:
   - `Question`: The FAQ questions
   - `Answer`: The corresponding answers

2. Use the file upload feature in the app to import your FAQ dataset

### Using the Chatbot
1. Once your FAQ data is uploaded, the chatbot is ready to answer questions
2. Type your question in the chat input
3. The chatbot will:
   - Search for relevant context in the uploaded FAQ data
   - Use Google's Gemini LLM to generate accurate, contextual responses
   - Provide answers based on the closest matching questions in the database

### Features
- **Semantic Search**: Finds relevant answers even when questions are phrased differently
- **Context-Aware**: Responses are based on the uploaded FAQ data
- **Real-time Processing**: Stream-based response generation
- **Distance-Based Filtering**: Only includes highly relevant context (similarity distance < 0.5)
