# AgriX Flask AI Backend

**Version:** 2.0.0  
**Port:** `5002`

AI-powered agricultural advisory services with automatic fallback mechanisms.

---

## ✨ Features

- **19 Route Files** with 48+ endpoints
- **Automatic Fallback** - If one AI provider fails, tries the next
- **Safe Loading** - Gracefully handles missing dependencies
- **Status API** - Monitor health and loaded routes
- **Multi-Language** - English, Hindi, Tamil, Telugu, Bengali, Marathi, Kannada, Gujarati

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python run.py
```

**Server URL:** `http://0.0.0.0:5002`

---

## 📊 API Routes Summary

### Core AI (Always Available)
| Route | Purpose |
|-------|---------|
| `/plant-disease` | Disease detection from images |
| `/crop_suggestion` | Crop recommendations |
| `/fertilizer` | Fertilizer advice |
| `/water_management` | Irrigation planning |
| `/crop_calendar` | Week-by-week schedule |
| `/advisory/ask` | AI farming Q&A |
| `/postharvest` | Storage & selling |
| `/govscheme` | Scheme summaries |
| `/translate` | Multi-language |
| `/api/weather-market` | Weather + market |

### External API Integrations
| Route | Provider | Key Required |
|-------|----------|--------------|
| `/gemini/*` | Google Gemini 2.5 Flash | `GOOGLE_API_KEY` |
| `/openrouter/*` | 300+ AI Models | `OPENROUTER_API_KEY` |
| `/huggingface/*` | AgriParam, aksara | `HUGGINGFACE_API_KEY` |
| `/perplexity/*` | Web Search AI | `PERPLEXITY_API_KEY` |
| `/ambee/*` | Weather, Soil, AQI | `AMBEE_API_KEY` |
| `/myscheme/*` | Govt Schemes | `MYSCHEME_API_KEY` |
| `/upag/*` | Agri Statistics | `UPAG_USERNAME/PASSWORD` |
| `/alu/*` | Satellite Imagery | Partner Program |

### System Endpoints
| Endpoint | Purpose |
|----------|---------|
| `/health` | Health check |
| `/api/status` | Detailed status |
| `/api/ai-fallback` | Unified AI with fallback |

---

## 🔄 Fallback Chain

When you call `/api/ai-fallback`, it tries providers in order:

```
Gemini → OpenRouter → HuggingFace → Groq
   ↓         ↓            ↓           ↓
  Fast    300+ Models   AgriParam   Ultra-fast
```

If a provider is not configured or fails, it automatically moves to the next.

---

## 🔑 Environment Setup

Copy `.env.example` to `.env`:

```bash
# Required
GROQ_API_KEY=gsk_xxx

# AI Providers (configure at least one)
GOOGLE_API_KEY=AIza_xxx          # Gemini
OPENROUTER_API_KEY=sk-or-v1-xxx  # GPT-4, Claude, Llama
HUGGINGFACE_API_KEY=hf_xxx       # AgriParam (FREE!)

# Optional Services
PERPLEXITY_API_KEY=pplx-xxx
AMBEE_API_KEY=xxx
MYSCHEME_API_KEY=xxx
UPAG_USERNAME=xxx
UPAG_PASSWORD=xxx
GOOGLE_ALU_API_KEY=xxx
```

---

## 📁 Project Structure

```
AiBackend/
├── app/
│   ├── __init__.py      # Flask factory with safe loading
│   ├── config.py        # Configuration
│   ├── routes/          # 19 route files
│   │   ├── gemini.py       # Gemini 2.5 Flash
│   │   ├── openrouter.py   # 300+ AI models
│   │   ├── huggingface.py  # Agricultural models
│   │   ├── ambee.py        # Environmental data
│   │   ├── perplexity.py   # Web search AI
│   │   ├── myscheme.py     # Govt schemes
│   │   ├── upag.py         # Agri stats
│   │   ├── alu.py          # Satellite imagery
│   │   └── ... (10 more)
│   └── chroma_db/       # Vector store
├── run.py               # Entry point
├── requirements.txt     # Python dependencies
├── API_DOCS.md          # Complete API reference
├── .env.example         # Environment template
└── .env                 # Your configuration (gitignored)
```

---

## 📚 Documentation

- [**API_DOCS.md**](./API_DOCS.md) - Complete endpoint reference
- [**Main README**](../README.md) - Project overview
- [**Backend README**](../backend/README.md) - Node.js backend

---

## 🧪 Testing

Check if everything is working:

```bash
# Health check
curl http://localhost:5002/health

# Detailed status
curl http://localhost:5002/api/status

# Test AI fallback
curl -X POST http://localhost:5002/api/ai-fallback \
  -H "Content-Type: application/json" \
  -d '{"message": "When to plant wheat in Punjab?"}'
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Route not loading | Check `/api/status` for failed blueprints |
| API key error | Verify key in `.env` is correct |
| 503 on HuggingFace | Model is warming up, retry in 30 seconds |
| CORS error | Frontend should call via `AIBACKEND_URL` |
