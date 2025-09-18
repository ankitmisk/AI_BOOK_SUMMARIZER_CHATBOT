# 📖 Premchand Story Summarizer

A hybrid app combining **Gemini AI** (for modern transformer summarization) and **Custom LSTM models** (trained on Premchand’s books) to generate summaries of Hindi/English stories.

---

## 🚀 Features
- Summarize Premchand’s books using **LSTM models**
- Summarize any custom story text using **Gemini AI**
- Multiple summary lengths: `short`, `medium`, `long`, `bullet`
- Option for **streaming word-by-word output**
- Download summary as `.txt`

---

## 🛠️ Installation

```bash
# Clone the repo
git clone https://github.com/your-username/premchand-story-summarizer.git
cd premchand-story-summarizer

# Create virtual env (recommended)
python -m venv venv
source venv/bin/activate   # on Linux/Mac
venv\Scripts\activate      # on Windows

# Install dependencies
pip install -r requirements.txt
