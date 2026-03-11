# Quick Start Guide - Step by Step

## ✅ Step 1: Create Environment File

Create a `.env` file in the project root (`multi-domain-rag-chatbot/.env`):

**Windows (Command Prompt):**
```cmd
cd multi-domain-rag-chatbot
echo GROQ_API_KEY=your_actual_api_key_here > .env
```

**Or manually create the file:**
1. Create a new file named `.env` in `multi-domain-rag-chatbot/` folder
2. Add this line (replace with your actual key):
   ```
   GROQ_API_KEY=gsk_your_actual_groq_api_key_here
   ```

Get your API key from: https://console.groq.com/

---

## ✅ Step 2: Start Backend Server

**Open Terminal 1:**

```cmd
cd multi-domain-rag-chatbot
venv\Scripts\activate
uvicorn src.app.main:app --reload --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**✅ Test Backend:**
- Open browser: http://localhost:8000/health
- Should show: `{"status":"ok"}`

**Keep this terminal open!**

---

## ✅ Step 3: Start Frontend Server

**Open a NEW Terminal 2:**

```cmd
cd multi-domain-rag-chatbot\frontend
npm install
npm run dev
```

**You should see:**
```
  VITE v5.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

**Keep this terminal open too!**

---

## ✅ Step 4: Open the Application

1. Open your browser
2. Go to: **http://localhost:5173**
3. You should see the home page with 3 domain cards:
   - 🎓 Education
   - 🏥 Medical  
   - ⚖️ Legal

4. Click on any domain to start chatting!

---

## 🎉 You're Done!

You now have:
- ✅ Backend running on port 8000
- ✅ Frontend running on port 5173
- ✅ Multi-domain chatbot ready to use!

---

## 🔧 Troubleshooting

**Backend won't start:**
- Make sure `.env` file exists with `GROQ_API_KEY=...`
- Make sure virtual environment is activated
- Check if port 8000 is already in use

**Frontend won't start:**
- Run `npm install` first
- Make sure backend is running on port 8000
- Check if port 5173 is already in use

**Can't connect:**
- Make sure both servers are running
- Check browser console for errors
- Verify backend health: http://localhost:8000/health

