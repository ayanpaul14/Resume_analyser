# 📄 AI Resume Analyser

A premium, responsive, and state-of-the-art AI-powered career dashboard. The application parses resume documents (PDF or TXT), evaluates key performance indicators, and generates structured executive feedback on formatting, action verbs, and target job alignment.

🚀 **Live Demo**: [https://resumeanalyser-3gtuveqksrjuazbnjnybkr.streamlit.app/](https://resumeanalyser-3gtuveqksrjuazbnjnybkr.streamlit.app/)

---

## ✨ Features

- **🌐 Multi-Provider AI Support**: Dynamically route requests between **Google Gemini (free tier)**, **OpenAI (GPT)**, or **xAI (Grok)**.
- **🎯 Visual Match Score Ring**: Dynamically computes a resume score (0-100) and displays it in a color-coded circular status component (Green for strong, Yellow for average, Red for weak match).
- **📊 Tabbed Executive Dashboard**: AI feedback is parsed and categorized into interactive tabs:
  - 📊 **Executive Summary**: Overview of visual impression and career pathing.
  - 💪 **Key Strengths**: Highlighted accomplishments and top skills.
  - 🔍 **Critical Gaps**: Constructive audit of formatting, syntax, and phrasing.
  - 🎯 **Recommendations**: Actionable step-by-step improvements tailored to the target role.
- **📥 Downloadable Markdown Reports**: Export your generated evaluation as a clean `.md` document with a single click.
- **🎨 Glassmorphic UI & Typography**: Custom styles featuring radial ambient lighting glows, card panels with backdrop blur, and modern fonts (**Space Grotesk** & **Plus Jakarta Sans**).
- **📱 Fully Responsive**: Custom CSS media queries align elements, scale sizes, and optimize navigation tabs for mobile thumbs.

---

## 🛠️ Tech Stack

- **Core**: Python 3.14 / Streamlit
- **Document Parsing**: `pypdf`
- **Integrations**: `openai` SDK (for OpenAI, Grok, and Gemini OpenAI-compatible endpoints)
- **Styling**: Custom CSS / HTML injection (supports responsive dark themes)

---

## 🚀 Local Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ayanpaul14/Resume_analyser.git
cd Resume_analyser
```

### 2. Configure Virtual Environment
Create a virtual environment and activate it:
```bash
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Secrets
Create a `.env` file in the root directory:
```env
# Google Gemini (Free tier key from https://aistudio.google.com)
GEMINI_API_KEY = "your-gemini-api-key"

# Grok (Paid key from https://console.x.ai)
GROK_API_KEY = "your-grok-api-key"

# OpenAI (Paid key from https://platform.openai.com)
OPENAI_API_KEY = "your-openai-api-key"
```

---

## 💻 Running the App Locally

Start the local Streamlit development server:
```bash
.venv\Scripts\python -m streamlit run main.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your web browser.

---

## ☁️ Deployment (Streamlit Community Cloud)

To host your app live on Streamlit Community Cloud:

1. Push your latest code to your public GitHub repository.
2. Sign in to **[Streamlit Community Cloud](https://share.streamlit.io/)** with your GitHub account.
3. Click **New App**, select your repo (`ayanpaul14/Resume_analyser`), and set the main file path to `main.py`.
4. Click **Advanced settings...** and paste your API keys in the **Secrets (TOML)** box:
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key"
   GROK_API_KEY = "your-grok-api-key"
   OPENAI_API_KEY = "your-openai-api-key"
   ```
5. Click **Deploy!**

---

## 🔒 Security
The project is configured with a `.gitignore` to prevent committing the `.env` configuration file containing private API keys to GitHub. Always use Streamlit Secrets or the UI password-masked inputs to override keys safely.
