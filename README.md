# 📄 AI Resume Career Advisor

A local-first web app that reads a PDF resume, extracts the structured details that matter, and generates personalised career advice — using an LLM that runs entirely on your own machine.

Built with **Flask**, **pdfplumber**, and a local model served through **LM Studio**. No API keys, no cloud costs, and no resume data leaving your computer.

---

## ✨ What it does

Upload a resume and the app will:

- 📑 Extract the raw text from the PDF, page by page
- 🧠 Ask a local LLM a series of focused questions about the candidate
- 👤 Pull out the **name** (verbatim, spelling preserved) and **email**
- 🛠️ List the **key technical skills** found in the resume
- 📝 Summarise the candidate's **work history** in two sentences
- 🎯 Suggest the **top 3 job titles** they should apply for
- 💡 Generate **full career advice** with an immediate next step
- 💾 Append every result to a CSV file so applications are never lost
- 🖥️ Show a friendly result card with the candidate's name and advice

---

## 🏗️ How it works

```text
PDF resume
    │
    ▼
pdfplumber  ──►  plain text
    │
    ▼
LM Studio (qwen/qwen3-vl-4b, local)
    │
    ├─► name
    ├─► email
    ├─► skills
    ├─► work-history summary
    ├─► top 3 job titles
    └─► career advice
    │
    ▼
resumes_data.csv  +  result page
```

1. The uploaded PDF is saved to `uploads/`.
2. `extract_text_from_pdf()` reads every page with **pdfplumber**.
3. `get_ai_data()` opens a single chat session with the model, seeded with a strict system prompt, and asks six questions one after another so the model keeps context.
4. The six answers are written as one row to `resumes_data.csv`.
5. The template renders the candidate's name and career advice.

The system prompt explicitly tells the model to stay concise, to return `NaN` when information is missing, and never to invent details — which keeps the extracted data honest.

---

## 🧰 Tech stack

| Layer | Technology |
|---|---|
| Web framework | Flask 3 |
| Templating | Jinja2 |
| PDF parsing | pdfplumber |
| Local LLM runtime | LM Studio Python SDK (`lmstudio`) |
| Model | `qwen/qwen3-vl-4b` (configurable) |
| Storage | CSV (flat file, no setup required) |
| Language | Python 3.11 |

---

## 📁 Project structure

```text
ResumeRecommender/
├── app.py                 # Flask app, PDF extraction, LLM prompting, CSV logging
├── templates/
│   └── index.html         # Upload page + result card
├── uploads/               # Uploaded PDF resumes (created automatically)
├── resumes_data.csv       # Extracted results (created automatically)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting started

### Prerequisites

- **Python 3.9+** (developed on 3.11)
- **[LM Studio](https://lmstudio.ai/)** installed
- A compatible model downloaded in LM Studio — the app defaults to `qwen/qwen3-vl-4b`

### 1. Clone the repository

```bash
git clone https://github.com/Sourajit1234/ResumeRecommender.git
cd ResumeRecommender
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the local model server

1. Open **LM Studio**.
2. Download and load `qwen/qwen3-vl-4b` (or any chat model you prefer).
3. Start the **local server** (default: `http://localhost:1234`).

> The `lmstudio` Python SDK connects to this local server automatically. If you switch models, update the model name in `get_ai_data()` inside `app.py`.

### 5. Run the app

```bash
python app.py
```

Open **http://127.0.0.1:5000**, upload a PDF resume, and click **Analyze Resume**.

---

## ⚙️ Configuration

All settings live at the top of `app.py`:

| Setting | Default | Purpose |
|---|---|---|
| `UPLOAD_FOLDER` | `uploads` | Where uploaded PDFs are stored |
| `CSV_FILE` | `resumes_data.csv` | Where extracted data is appended |
| Model name | `qwen/qwen3-vl-4b` | Local model used for analysis |

The CSV is created automatically with this header:

```text
Name, Email, Skills, Summary, Job Titles, Advice
```

---

## ⚠️ Limitations

- Only **PDF** files are supported (no DOCX or scanned images yet).
- The app processes requests **synchronously**, so analysis time depends on your hardware.
- Prompts are tuned for the default Qwen model; a very small model may return inconsistent formatting.
- There is no authentication or database — it is designed as a single-user local tool.

## 🗺️ Roadmap

- [ ] Batch upload and processing of multiple resumes
- [ ] Job-description matching and a ranked candidate shortlist
- [ ] DOCX and scanned-PDF (OCR) support
- [ ] A results dashboard instead of plain CSV
- [ ] Configurable prompts and model selection from the UI

---

## 👤 Author

**Sourajit Mandal**

- GitHub: [@Sourajit1234](https://github.com/Sourajit1234)

---

⭐ If you found this project useful, consider giving it a star!
