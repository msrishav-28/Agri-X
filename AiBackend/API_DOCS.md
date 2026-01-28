# AgriX AI Backend API Documentation

**Version:** 2.0.0  
**Base URL:** `http://YOUR_IP:5002`

---

## 📊 Quick Summary

| Category | Routes | Endpoints |
|----------|--------|-----------|
| Core AI | 10 | 12 |
| External APIs | 8 | 33 |
| System | 3 | 3 |
| **Total** | **19** | **48** |

---

## 🏥 System Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/status` | GET | Detailed status with loaded routes & API keys |
| `/api/ai-fallback` | POST | **Unified AI with automatic fallback** |

### AI Fallback Chain
The `/api/ai-fallback` endpoint automatically tries providers in order:
1. **Gemini 2.5 Flash** (if `GOOGLE_API_KEY` configured)
2. **OpenRouter** (if `OPENROUTER_API_KEY` configured)
3. **HuggingFace AgriParam** (if `HUGGINGFACE_API_KEY` configured)
4. **Groq** (if `GROQ_API_KEY` configured)

---

## 🤖 Core AI Routes

### 1. Plant Disease Detection
**File:** `plant_disease.py` | **Uses:** Groq

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/plant-disease` | POST | Analyze plant image for diseases |

**Request:**
```json
{
  "image": "base64_encoded_image",
  "language": "Hindi"
}
```

---

### 2. Crop Suggestions
**File:** `crop_suggestion.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/crop_suggestion` | POST | Get crop recommendations |

---

### 3. Fertilizer Recommendations
**File:** `fertilizer.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/fertilizer_recommendation` | POST | Get fertilizer advice |

---

### 4. Water Management
**File:** `water_management.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/water_management` | POST | Irrigation recommendations |

---

### 5. Crop Calendar
**File:** `crop_calendar.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/crop_calendar` | POST | Week-by-week farming plan |

---

### 6. Agricultural Advisory
**File:** `agri_advisory.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/advisory/ask` | POST | AI farming Q&A |

---

### 7. Post-Harvest Planning
**File:** `postharvest.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/postharvest` | POST | Storage & selling advice |

---

### 8. Government Schemes
**File:** `govscheme.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/govscheme` | POST | Summarize schemes |

---

### 9. Translation
**File:** `translate.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/translate` | POST | Multi-language translation |

---

### 10. Market Data
**File:** `market.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/weather-market` | GET | Weather + market data |

---

## 🔌 External API Integrations

### 11. Gemini 2.5 Flash
**File:** `gemini.py` | **Key:** `GOOGLE_API_KEY` ✅

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/gemini/chat` | POST | AI chat with context |
| `/gemini/analyze-image` | POST | Vision analysis |
| `/gemini/farming-advice` | POST | Personalized advice |
| `/gemini/translate` | POST | Agricultural translation |
| `/gemini/status` | GET | Check status |

---

### 12. OpenRouter (300+ Models)
**File:** `openrouter.py` | **Key:** `OPENROUTER_API_KEY` ✅

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/openrouter/chat` | POST | Chat with GPT-4, Claude, Llama, etc. |
| `/openrouter/vision` | POST | Image analysis |
| `/openrouter/models` | GET | List available models |
| `/openrouter/compare` | POST | Compare model responses |
| `/openrouter/status` | GET | Check status |

**Model Presets:** `fast`, `balanced`, `smart`, `premium`, `vision`

---

### 13. Hugging Face (Agricultural Models)
**File:** `huggingface.py` | **Key:** `HUGGINGFACE_API_KEY` 🆓

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/huggingface/chat` | POST | Chat with AgriParam, aksara |
| `/huggingface/disease-detect` | POST | Plant disease classifier |
| `/huggingface/crop-recommend` | POST | Soil-based recommendations |
| `/huggingface/models` | GET | List agricultural models |
| `/huggingface/status` | GET | Check status |

**Available Models:** `agriparam`, `aksara`, `agri-llama`, `plant-disease`

---

### 14. Perplexity (Web Search AI)
**File:** `perplexity.py` | **Key:** `PERPLEXITY_API_KEY` ✅

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/perplexity/chat` | POST | AI with real-time web search |

---

### 15. Ambee (Environmental Data)
**File:** `ambee.py` | **Key:** `AMBEE_API_KEY` ✅

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ambee/weather/latest` | POST | Real-time weather |
| `/ambee/weather/forecast` | POST | Weather forecast |
| `/ambee/soil` | POST | Soil moisture & temp |
| `/ambee/air-quality` | POST | AQI data |
| `/ambee/pollen` | POST | Pollen count |
| `/ambee/fire` | POST | Wildfire alerts |
| `/ambee/disasters` | POST | Natural disasters |
| `/ambee/farming-dashboard` | POST | **All data + AI insights** |
| `/ambee/status` | GET | Check status |

---

### 16. myScheme (Government Schemes)
**File:** `myscheme.py` | **Key:** `MYSCHEME_API_KEY`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/myscheme/search` | POST | Search schemes |
| `/myscheme/eligibility` | POST | Check eligibility |
| `/myscheme/agriculture` | GET | List agriculture schemes |

---

### 17. UPAg (Agricultural Statistics)
**File:** `upag.py` | **Keys:** `UPAG_USERNAME`, `UPAG_PASSWORD`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upag/login` | POST | OAuth2 login |
| `/upag/sources` | GET | List data sources |
| `/upag/data/<source>` | POST | Get data from source |
| `/upag/crop-prices` | POST | Mandi prices |
| `/upag/crop-production` | POST | Production data |

---

### 18. Google ALU (Satellite Imagery)
**File:** `alu.py` | **Key:** `GOOGLE_ALU_API_KEY` (Partner Program)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/alu/crop-health` | POST | NDVI, crop stress |
| `/alu/field-boundary` | POST | Field detection |
| `/alu/crop-classification` | POST | Crop type ID |
| `/alu/yield-prediction` | POST | Harvest forecast |
| `/alu/status` | GET | Check status |

> **Note:** Returns mock data if API key not configured (demo mode)

---

## 🔑 Environment Variables

```bash
# Core AI
GROQ_API_KEY=gsk_xxx
GOOGLE_API_KEY=AIza_xxx

# AI Providers
OPENROUTER_API_KEY=sk-or-v1-xxx
HUGGINGFACE_API_KEY=hf_xxx
PERPLEXITY_API_KEY=pplx-xxx

# Environmental Data
AMBEE_API_KEY=xxx

# Government APIs
MYSCHEME_API_KEY=xxx
UPAG_USERNAME=xxx
UPAG_PASSWORD=xxx

# Satellite (Partner Program)
GOOGLE_ALU_API_KEY=xxx
```

---

## 🚀 Quick Start

```bash
cd AiBackend
pip install -r requirements.txt
python run.py
```

**Server:** `http://0.0.0.0:5002`

**Check Status:** `GET /api/status`

---

## 💡 Fallback Strategy

If an API fails or isn't configured:

| Feature | Primary | Fallback 1 | Fallback 2 |
|---------|---------|------------|------------|
| AI Chat | Gemini | OpenRouter | HuggingFace |
| Disease Detection | Gemini Vision | HuggingFace | Groq |
| Weather | Ambee | Open-Meteo | - |
| Schemes | myScheme API | Local data | - |
| Satellite | Google ALU | Mock data | - |
