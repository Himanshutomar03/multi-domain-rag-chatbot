# How to Run the Multi-Domain RAG Chatbot

This guide will walk you through setting up and running both the backend and frontend of the chatbot.

## Prerequisites

- **Python 3.8+** installed
- **Node.js 16+** and **npm** (or yarn/pnpm) installed
- **GROQ API Key** (get one from https://console.groq.com/)

## Step 1: Backend Setup

### 1.1 Navigate to Project Root
```bash
cd multi-domain-rag-chatbot
```

### 1.2 Create Virtual Environment (Recommended)
**Important:** Using a virtual environment prevents dependency conflicts with other Python packages (like Spyder) installed globally.

**Windows:**
```bash
# Option 1: Use the setup script
setup_venv.bat

# Option 2: Manual setup
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Note:** If you see dependency conflict warnings (like Spyder/IPython), using a virtual environment will resolve them.

### 1.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 1.4 Create Environment File
Create a `.env` file in the project root (`multi-domain-rag-chatbot/.env`):

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your actual GROQ API key.

### 1.5 Verify Vector Stores
Make sure you have vector stores in the `vectorstores` directory:
- `vectorstores/education_faiss/` (should exist)
- `vectorstores/medical_faiss/` (create if needed)
- `vectorstores/legal_faiss/` (create if needed)

**Note:** If medical or legal vector stores don't exist, those domains will show errors. You can still use the education domain.

### 1.6 Start the Backend Server
```bash
uvicorn src.app.main:app --reload --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

The backend API is now running at `http://localhost:8000`

**Test the backend:**
- Open browser: `http://localhost:8000/health`
- Should return: `{"status":"ok"}`

## Step 2: Frontend Setup

### 2.1 Navigate to Frontend Directory
Open a **new terminal window** (keep backend running) and navigate to:
```bash
cd multi-domain-rag-chatbot/frontend
```

### 2.2 Install Frontend Dependencies
```bash
npm install
```

This will install:
- React
- React Router DOM
- Vite
- TypeScript
- And other dependencies

### 2.3 (Optional) Configure API URL
If your backend is running on a different URL, create a `.env` file in the `frontend` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

By default, the frontend expects the backend at `http://localhost:8000`.

### 2.4 Start the Frontend Development Server
```bash
npm run dev
```

You should see output like:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Step 3: Access the Application

1. Open your browser and go to: **http://localhost:5173**

2. You'll see the home page with three domain cards:
   - **Education** (cyan/blue)
   - **Medical** (red)
   - **Legal** (teal)

3. Click on any domain card or use the navigation bar to switch between domains.

4. Start chatting! Each domain has its own chat interface.

## Running Both Servers

You need **two terminal windows**:

**Terminal 1 (Backend):**
```bash
cd multi-domain-rag-chatbot
# Activate venv if using one
uvicorn src.app.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd multi-domain-rag-chatbot/frontend
npm run dev
```

## Troubleshooting

### Backend Issues

**Dependency Conflict Warnings (Spyder/IPython):**
- This is a warning, not an error - the project will still work
- **Solution:** Use a virtual environment (see Step 1.2) to isolate dependencies
- The project doesn't use Spyder, so this conflict won't affect functionality
- If you see this warning, you can safely ignore it OR use a virtual environment

**Error: "GROQ_API_KEY is missing from .env"**
- Make sure `.env` file exists in `multi-domain-rag-chatbot/` directory
- Check that the file contains: `GROQ_API_KEY=your_actual_key`

**Error: "Vector store not found"**
- For education: Make sure `vectorstores/education_faiss/` exists
- For medical/legal: Create the vector stores or the domains will show errors
- You can still use the education domain if others are missing

**Port 8000 already in use:**
- Change the port: `uvicorn src.app.main:app --reload --port 8001`
- Update frontend `.env` to match: `VITE_API_BASE_URL=http://localhost:8001`

### Frontend Issues

**Error: "Cannot find module 'react-router-dom'"**
- Run: `npm install` in the `frontend` directory

**Frontend can't connect to backend:**
- Make sure backend is running on port 8000
- Check `frontend/vite.config.ts` proxy settings
- Verify CORS is enabled in backend (it should be)

**Port 5173 already in use:**
- Vite will automatically use the next available port
- Or specify: `npm run dev -- --port 5174`

### General Issues

**Module not found errors:**
- Backend: `pip install -r requirements.txt`
- Frontend: `npm install`

**Python version issues:**
- Make sure you're using Python 3.8 or higher
- Check with: `python --version` or `python3 --version`

## Production Build

### Build Frontend
```bash
cd frontend
npm run build
```

This creates a `dist/` folder with production-ready files.

### Serve Frontend (Production)
```bash
npm run preview
```

## API Endpoints

- `GET /health` - Health check
- `POST /api/chat` - Chat endpoint
  ```json
  {
    "message": "Your question here",
    "domain": "education" | "medical" | "legal"
  }
  ```

## Quick Start Summary

```bash
# Terminal 1: Backend
cd multi-domain-rag-chatbot
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
# Create .env with GROQ_API_KEY
uvicorn src.app.main:app --reload --port 8000

# Terminal 2: Frontend
cd multi-domain-rag-chatbot/frontend
npm install
npm run dev
```

Then open: **http://localhost:5173**

