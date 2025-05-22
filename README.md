# 🧠 Panelize Backend

The backend for **Panelize**, an AI-powered comic book and manga panel generator. This Flask-based server takes in user-written stories and returns a sequence of AI-generated images with captions — powered by **GPT-4o**, **DALL·E 3**, and **BLIP**.

---

## 🛠️ Technologies Used

- 🐍 **Python 3.10+**
- 🔥 **Flask** — lightweight REST API framework
- 🤖 **OpenAI API (GPT-4o & DALL·E 3)** — for prompt engineering and image generation
- 🧠 **Hugging Face Transformers** — for BLIP image captioning
- 🖼️ **Pillow (PIL)** — for image processing
- 🌐 **CORS** — to allow frontend interaction
- 🧪 **Requests** — for image retrieval from OpenAI URLs

---

## ✨ Features

- 🔗 Story decomposition into sequential panel prompts using GPT-4o
- 🎨 Image generation with DALL·E 3 in chosen art styles (manga, comic book, custom)
- 🖋️ Image captioning with BLIP to inform chained prompts
- 🔁 Prompt chaining logic to maintain visual-narrative flow across panels
- 📦 REST API returns panel prompts, images, and captions as JSON
- 🔐 API key handling via environment variables

---

## 📦 Local Setup

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/panelize_backend.git
cd panelize_backend
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .\.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Your OpenAI API Key
```bash
# Linux/macOS
export OPENAI_API_KEY=your-key-here

# Windows PowerShell
$env:OPENAI_API_KEY="your-key-here"
```

---

## 🚀 Running the Server

### Local Development
```bash
flask run
```
Server will be live at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Production/Render Deployment
```bash
gunicorn app:app --bind 0.0.0.0:5000
```
This is the recommended command for deploying on Render or any production server.

---

## 📡 API Usage

### POST `/api/generate-panels`

**Request:**
```json
{
  "story_description": "A samurai travels through time and meets a future AI...",
  "num_panels": 3,
  "style": "manga"
}
```

**Response:**
```json
{
  "panels": [
    {
      "prompt": "In colored manga theme generate the following: ...",
      "image_url": "https://...",
      "caption": "A lone samurai stands in a neon-lit alley..."
    },
    ...
  ]
}
```

---

## 🧠 Project Structure

```
panelize_backend/
├── app.py                    # Main Flask app entry
├── routes/
│   └── panel_routes.py       # API routes
├── services/
│   └── openai_service.py     # GPT/DALL·E/BLIP logic
├── requirements.txt
└── .env                      # Optional OpenAI API key
```

---

## 📝 License

MIT License © 2025 Anthony Lamelas
