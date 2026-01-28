# AgriX: See, Detect, Protect

> Empowering Indian farmers with AI-driven, localized, multilingual agricultural companion.

---

## Our Mission

Agriculture forms the backbone of India’s economy, yet smallholder farmers lack access to localized, real-time farming advice, government schemes, and smart market insights.  
**AgriX** addresses this gap with AI-powered, voice-enabled solutions tailored to empower every Indian farmer.

---

## Objective

**Goal:**  
- Deliver **personalized crop, weather, and market advice** to farmers in **regional languages**.
- **Simplify access** to **government schemes**, **fertilizer recommendations**, and **post-harvest planning**.
- Using **powerful AI** for **natural language advisory, smart recommendations, and document summarization**.

---

### Our Approach:

- Focused on real-world impact for rural India.
- Built a multilingual, intuitive UI with **voice navigation**.
- Integrated APIs like **Open Meteo**, **Data.gov.in**, **ISRIC**.
- Used **Groq’s ultra-fast LLMs** for **RAG (Retrieval Augmented Generation)** based dynamic advisory.
- Optimized AI calls to keep app lightweight and affordable for farmers.

---

## Tech Stack

### Core Technologies:

-   **Frontend:** ![React Native](https://img.shields.io/badge/React_Native-20232A?style=for-the-badge&logo=react&logoColor=61DAFB) ![React Navigation](https://img.shields.io/badge/React_Navigation-8b5cf6?style=for-the-badge&logo=react&logoColor=white)
-   **Backend:** ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)
-   **AI Engine:** ![Google Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-8E75B2?style=for-the-badge&logo=google&logoColor=white) ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white) ![Groq](https://img.shields.io/badge/Groq-FF6B35?style=for-the-badge)
-   **Database:** ![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
-   **Authentication:** ![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

### API Integrations:

| API | Purpose | Status |
|-----|---------|--------|
| **Gemini 2.5 Flash** | AI Chat, Vision, Translation | ✅ Configured |
| **OpenRouter** | 300+ AI Models (GPT-4, Claude, Llama) | ✅ Configured |
| **Hugging Face** | AgriParam, Plant Disease Classifier | 🆓 FREE |
| **Groq** | Fast LLM inference | ✅ Configured |
| **Perplexity** | Web-search AI | ✅ Configured |
| **Ambee** | Weather, Soil, Air Quality | ✅ Configured |
| **Open-Meteo** | Weather forecasts | ✅ Ready |
| **Data.gov.in** | Market prices | ✅ Ready |
| **myScheme** | Govt scheme eligibility | 🔑 Needs Key |
| **UPAg** | Agricultural statistics | 🔑 Needs Key |
| **Google ALU** | Satellite imagery | 🔑 Partner Program |

### Hosting:
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

---

## Key Features

-  **Modern & Intuitive UI:** A clean, vibrant interface with beautiful **glassmorphic** elements and **engaging animations** that make the app easy and delightful to use.
-  **Agentic RAG Advisory Chatbot:** Get answers to your farming queries through a smart, conversational AI.
-  **Crop Disease Detection:** Upload an image of your crop to get instant disease detection and health analysis.
-  **Personalized Fertilizer Recommendations:** Receive tailored fertilizer suggestions based on your crop and soil data.
-  **Post-Harvest Planning** with Google Calendar sync.
-  **Smart Market Analysis:** Access real-time market prices, trend predictions, and AI-driven analysis.
-  **Dynamic Crop Calendar:** Generate detailed, week-by-week action plans for your chosen crops.
-  **Multilingual Voice Navigation:** Navigate the app and access information using your voice in your preferred language.
-  **Government Schemes Summarizer:** Understand complex government schemes through simple, clear summaries.
-  **Real-time Weather Forecasts:** Stay updated with the latest weather information for your location.

---

## Supported Languages

AgriX supports **8 languages**:

-   English
-   Hindi (हिंदी)
-   Marathi (मराठी)
-   Tamil (தமிழ்)
-   Bengali (বাংলা)
-   Kannada (ಕನ್ನಡ)
-   Telugu (తెలుగు)
-   Malayalam (മലയാളം)

---

- **Demo Video Link:** [Watch Here]()

---

## App Screenshots


<div style="display: flex; justify-content: space-around;">
  <img src="./README_assets/home.jpg" alt="Home Screen" width="30%" />
  <img src="./README_assets/cropcare1.jpg" alt="Crop Disease Detection" width="30%" />
  <img src="./README_assets/cropcare2.jpg" alt="Crop Disease Detection" width="30%" />
</div>
<br />
<div style="display: flex; justify-content: space-around;">
  <img src="./README_assets/market1.jpg" alt="market" width="30%" />
  <img src="./README_assets/water1.jpg" alt="market" width="30%" />
  <img src="./README_assets/water2.jpg" alt="market" width="30%" />
</div>
<br />
<div style="display: flex; justify-content: space-around;">
  <img src="./README_assets/news.jpg" alt="news" width="30%" />
  <img src="./README_assets/market2.jpg" alt="market" width="30%" />
  <img src="./README_assets/market3.jpg" alt="market" width="30%" />
</div>

---

## How to Run the Project

### Requirements:

- Node.js v18+
- Python 3.11.0
- MongoDB Atlas or Local
- Groq API Key
- An `.env` configuration file (see `.env.example`).

Here's the updated local setup instructions with the corrected folder structure and descriptions for your project:

---

## Local Setup

## Clone the repository

```bash
git clone [https://github.com/msrishav-28/nila-shoshsho](https://github.com/msrishav-28/nila-shoshsho)
```

## Install dependencies and run the applications

### 1. **Frontend (React Native - Mobile App)**

Navigate to the `MobileApp` folder and install the required dependencies:

```bash
cd MobileApp
npm install
```

Then, start the mobile app:

```bash
npx react-native run-android
```

### 2. **Backend (Node.js)**

Navigate to the `backend` folder and install the Node.js dependencies:

```bash
cd ../backend
npm install
```

Start the backend:

```bash
npm run dev
```

### 3. **AiBackend (Python)**

Navigate to the `AiBackend` folder and install the Python dependencies:

```bash
cd ../AiBackend
pip install -r requirements.txt
```

Run the AI backend:

```bash
flask run
```

---

## Future Scope

- **Satellite Integration:** Satellite-driven analysis for soil moisture and crop stress.
- Expansion to Bangladesh, Nepal, Sri Lanka (regional adaptations).
- **Blockchain for Data Privacy:** A long-term vision to secure farmer data.
- **Offline Support:** Access critical information even without an active internet connection through periodic syncing.
- **Push Notifications:** Receive timely alerts for market price changes, weather warnings, and crop calendar reminders.
- **Enhanced Personalization:** A user profile section to tailor content based on your specific crops and preferences.
- **Improved Accessibility (a11y):** Full support for screen readers and other assistive technologies.
---

## Resources / Credits

### AI & ML
- [Google Gemini 2.5 Flash](https://ai.google.dev/) - Vision & Language AI
- [Groq](https://groq.com/) - Fast LLM Inference
- [LangChain](https://langchain.com/) - AI Framework
- [Perplexity](https://www.perplexity.ai/) - Web Search AI

### Environmental Data
- [Ambee](https://www.getambee.com/) - Weather, Soil, Air Quality
- [Open-Meteo](https://open-meteo.com/) - Weather Forecasts

### Agricultural Data
- [Data.gov.in](https://data.gov.in/) - Market Prices
- [UPAg](https://data.upag.gov.in/) - Agricultural Statistics
- [myScheme](https://www.myscheme.gov.in/) - Government Schemes
- [ISRIC](https://www.isric.org/) - Soil Data

### Satellite & Mapping
- Google ALU (Agriculture Landscape Understanding)

### Design
- Canva for Workflow Diagrams


---

## Final Words

**AgriX** stands for every farmer, helping them thrive using the power of AI, Groq, and community-driven innovation.

Let's sow the seeds of a smarter tomorrow, together!

---

# Thank you!
