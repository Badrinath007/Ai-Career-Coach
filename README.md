#  AI Career Coach

An intelligent career guidance tool that uses Natural Language Processing (NLP) to analyze resumes and job descriptions. It helps users identify skill gaps, improve job alignment, and receive actionable career recommendations.

---

## 🚀 Features

- 📄 Upload resume and/or paste job description
- 🧠 NLP-based skill and keyword extraction (using spaCy, NLTK, and BERT)
- 🔍 Semantic matching between resume and job description
- 📊 Skill gap analysis and improvement tips
- 🌐 Responsive frontend using HTML + Tailwind CSS
- 💡 Personalized career suggestions

---

## 📁 Project Structure

```
ai-career-coach/
│
├── backend/               # Python FastAPI/Flask backend
│   └── main.py            # Backend app entry point
│
├── frontend/              # Static frontend files
│   ├── index.html
│   └── assets/
│       └── styles.css     # Tailwind CSS
│
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container setup
├── README.md
└── .gitignore
```

---

## 🧰 Tech Stack

- **Frontend:** HTML, Tailwind CSS  
- **Backend:** Python (FastAPI or Flask)  
- **NLP:** spaCy, NLTK, Sentence-Transformers  
- **Deployment:** Docker (optional: Heroku/Netlify for frontend/backend separation)

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-career-coach.git
cd ai-career-coach
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Backend Server

```bash
uvicorn backend.main:app --reload
```

Or, for Flask:

```bash
python backend/main.py
```

### 4. Open `frontend/index.html` in your browser

Serve with a local server if needed.

---

## 🐳 Docker (Optional)

To build and run with Docker:

```bash
docker build -t ai-career-coach .
docker run -p 8000:8000 ai-career-coach
```

---

## 📌 Future Scope

- Personalized user accounts
- Multilingual support
- Career path prediction
- Advanced AI models for deeper analysis
- Real-time resume improvement feedback

---

## 📖 License

MIT License. See [LICENSE](LICENSE) for more information.

---

## 🙌 Acknowledgments

- [spaCy](https://spacy.io)
- [NLTK](https://www.nltk.org/)
- [SentenceTransformers](https://www.sbert.net/)
- [Tailwind CSS](https://tailwindcss.com/)
