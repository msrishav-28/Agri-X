from flask import Blueprint, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

openrouter_bp = Blueprint('openrouter_bp', __name__)

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Available models for agriculture use
RECOMMENDED_MODELS = {
    "fast": "mistralai/mistral-7b-instruct:free",           # Free, fast
    "balanced": "meta-llama/llama-3-8b-instruct:free",      # Free, good quality
    "smart": "google/gemini-2.0-flash-exp:free",            # Free, multimodal
    "premium": "anthropic/claude-3.5-sonnet",               # Paid, best quality
    "coding": "deepseek/deepseek-coder",                    # Good for technical
    "vision": "google/gemini-2.0-flash-exp:free"            # Image understanding
}

# Agricultural system prompts
AGRI_SYSTEM_PROMPT = """You are an expert agricultural advisor for Indian farmers.
Provide practical, actionable advice on:
- Crop management and best practices
- Pest and disease identification and treatment
- Fertilizer and irrigation recommendations
- Government schemes and subsidies
- Market prices and selling strategies
- Weather-based farming decisions

Keep responses concise, practical, and in simple language farmers can understand.
Include specific quantities, timings, and costs when relevant."""


@openrouter_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@openrouter_bp.route("/openrouter/chat", methods=["POST"])
def openrouter_chat():
    """
    Chat with any AI model through OpenRouter
    Supports 300+ models including GPT-4, Claude, Gemini, Llama, etc.
    """
    try:
        data = request.json
        message = data.get("message", "")
        model = data.get("model", "fast")  # Use preset or full model ID
        lang = data.get("lang", "English")
        history = data.get("history", [])
        custom_system = data.get("system_prompt")
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        if not OPENROUTER_API_KEY:
            return jsonify({"error": "OpenRouter API key not configured"}), 500
        
        # Resolve model preset to actual model ID
        model_id = RECOMMENDED_MODELS.get(model, model)
        
        # Build system prompt
        system_prompt = custom_system or AGRI_SYSTEM_PROMPT
        system_prompt += f"\n\nRespond in {lang} language."
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        for h in history:
            messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
        messages.append({"role": "user", "content": message})
        
        # Call OpenRouter API (OpenAI-compatible format)
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://agrix.app",  # Required by OpenRouter
                "X-Title": "AgriX Agricultural Assistant"
            },
            json={
                "model": model_id,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2048
            },
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        
        return jsonify({
            "success": True,
            "response": answer,
            "model": model_id,
            "usage": result.get("usage", {})
        }), 200
        
    except requests.exceptions.RequestException as e:
        print(f"OpenRouter API Error: {str(e)}")
        return jsonify({"error": "Error communicating with OpenRouter API"}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@openrouter_bp.route("/openrouter/vision", methods=["POST"])
def openrouter_vision():
    """
    Analyze images using vision-capable models
    Good for plant disease detection, crop identification
    """
    try:
        data = request.json
        image_url = data.get("image_url")  # URL or base64 data URL
        image_base64 = data.get("image_base64")
        query = data.get("query", "Analyze this plant image for diseases or health issues.")
        model = data.get("model", "google/gemini-2.0-flash-exp:free")
        lang = data.get("lang", "English")
        
        if not image_url and not image_base64:
            return jsonify({"error": "image_url or image_base64 required"}), 400
        
        if not OPENROUTER_API_KEY:
            return jsonify({"error": "OpenRouter API key not configured"}), 500
        
        # Build image content
        if image_base64:
            image_content = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        else:
            image_content = {"type": "image_url", "image_url": {"url": image_url}}
        
        system_prompt = f"""You are a plant pathology expert analyzing crop images.
        Provide:
        1. Plant/crop identification
        2. Health assessment (healthy/diseased)
        3. If diseased: disease name, severity (mild/moderate/severe), treatment
        4. Prevention recommendations
        
        Be specific about treatments including product names and dosages.
        Respond in {lang} language."""
        
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://agrix.app",
                "X-Title": "AgriX Plant Disease Detection"
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": query},
                            image_content
                        ]
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 2048
            },
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        analysis = result["choices"][0]["message"]["content"]
        
        return jsonify({
            "success": True,
            "analysis": analysis,
            "model": model
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@openrouter_bp.route("/openrouter/models", methods=["GET"])
def list_models():
    """
    Get list of available models from OpenRouter
    """
    try:
        if not OPENROUTER_API_KEY:
            # Return recommended models without API call
            return jsonify({
                "success": True,
                "recommended": RECOMMENDED_MODELS,
                "note": "Get full list by configuring OPENROUTER_API_KEY"
            }), 200
        
        response = requests.get(
            f"{OPENROUTER_BASE_URL}/models",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
            timeout=30
        )
        response.raise_for_status()
        
        models = response.json().get("data", [])
        
        # Filter to relevant models for agriculture
        free_models = [m for m in models if ":free" in m.get("id", "")]
        
        return jsonify({
            "success": True,
            "total_models": len(models),
            "free_models": len(free_models),
            "recommended": RECOMMENDED_MODELS,
            "all_models": models[:50]  # Limit response size
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@openrouter_bp.route("/openrouter/compare", methods=["POST"])
def compare_models():
    """
    Compare responses from multiple models for the same query
    Useful for testing which model works best
    """
    try:
        data = request.json
        message = data.get("message", "")
        models = data.get("models", ["fast", "balanced", "smart"])
        lang = data.get("lang", "English")
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        if not OPENROUTER_API_KEY:
            return jsonify({"error": "OpenRouter API key not configured"}), 500
        
        results = []
        
        for model_preset in models[:3]:  # Max 3 comparisons
            model_id = RECOMMENDED_MODELS.get(model_preset, model_preset)
            
            try:
                response = requests.post(
                    f"{OPENROUTER_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://agrix.app",
                        "X-Title": "AgriX Model Comparison"
                    },
                    json={
                        "model": model_id,
                        "messages": [
                            {"role": "system", "content": f"{AGRI_SYSTEM_PROMPT}\nRespond in {lang}."},
                            {"role": "user", "content": message}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1024
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    results.append({
                        "model": model_id,
                        "preset": model_preset,
                        "response": result["choices"][0]["message"]["content"],
                        "usage": result.get("usage", {})
                    })
                else:
                    results.append({
                        "model": model_id,
                        "preset": model_preset,
                        "error": f"Status {response.status_code}"
                    })
                    
            except Exception as e:
                results.append({
                    "model": model_id,
                    "preset": model_preset,
                    "error": str(e)
                })
        
        return jsonify({
            "success": True,
            "query": message,
            "comparisons": results
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@openrouter_bp.route("/openrouter/status", methods=["GET"])
def openrouter_status():
    """Check OpenRouter API configuration status"""
    return jsonify({
        "configured": bool(OPENROUTER_API_KEY),
        "endpoints": [
            "/openrouter/chat",
            "/openrouter/vision",
            "/openrouter/models",
            "/openrouter/compare"
        ],
        "recommended_models": RECOMMENDED_MODELS,
        "note": "Get API key at: https://openrouter.ai/keys"
    }), 200
