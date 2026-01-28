from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

gemini_bp = Blueprint('gemini_bp', __name__)

# Google Gemini API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini client
try:
    from google import genai
    client = genai.Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None
except ImportError:
    client = None
    print("Warning: google-genai not installed. Run: pip install google-genai")


@gemini_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# System prompts for different agricultural contexts
SYSTEM_PROMPTS = {
    "general": """You are an expert agricultural advisor for Indian farmers. 
    Provide practical, actionable advice on farming, crops, weather, pests, and market prices.
    Always consider local conditions and traditional knowledge.
    Respond in simple language that farmers can understand.
    Keep responses concise but comprehensive.""",
    
    "disease": """You are a plant pathology expert. Analyze crop diseases and provide:
    1. Disease identification
    2. Causes and spread patterns
    3. Organic and chemical treatment options
    4. Prevention measures
    Be specific about dosages and application methods.""",
    
    "market": """You are an agricultural market analyst. Provide:
    1. Price trends and predictions
    2. Best time to sell crops
    3. Market opportunities
    4. Storage advice if prices are low
    Base advice on current market conditions.""",
    
    "weather": """You are an agricultural meteorologist. Provide:
    1. Weather impact on farming activities
    2. Crop protection measures
    3. Optimal timing for planting, irrigation, harvesting
    4. Climate adaptation strategies"""
}


@gemini_bp.route("/gemini/chat", methods=["POST"])
def gemini_chat():
    """
    General agricultural chat using Gemini 2.5 Flash
    """
    try:
        data = request.json
        message = data.get("message", "")
        context = data.get("context", "general")  # general, disease, market, weather
        lang = data.get("lang", "English")
        history = data.get("history", [])  # Previous conversation
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        if not client:
            return jsonify({"error": "Gemini API not configured"}), 500
        
        # Build system prompt
        system_prompt = SYSTEM_PROMPTS.get(context, SYSTEM_PROMPTS["general"])
        system_prompt += f"\n\nRespond in {lang} language."
        
        # Build conversation
        contents = []
        for h in history:
            contents.append({"role": h.get("role", "user"), "parts": [{"text": h.get("content", "")}]})
        contents.append({"role": "user", "parts": [{"text": message}]})
        
        # Call Gemini 2.5 Flash
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config={
                "system_instruction": system_prompt,
                "temperature": 0.7,
                "max_output_tokens": 2048
            }
        )
        
        return jsonify({
            "success": True,
            "response": response.text,
            "model": "gemini-2.5-flash",
            "context": context
        }), 200
        
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@gemini_bp.route("/gemini/analyze-image", methods=["POST"])
def analyze_image():
    """
    Analyze crop/plant images using Gemini 2.5 Flash vision
    """
    try:
        data = request.json
        image_base64 = data.get("image")  # Base64 encoded image
        query = data.get("query", "Analyze this plant image and identify any diseases or health issues.")
        lang = data.get("lang", "English")
        
        if not image_base64:
            return jsonify({"error": "Image is required"}), 400
        
        if not client:
            return jsonify({"error": "Gemini API not configured"}), 500
        
        system_prompt = f"""You are a plant disease expert analyzing an image.
        Provide:
        1. Plant/crop identification
        2. Health assessment (healthy/diseased)
        3. If diseased: disease name, severity, treatment
        4. Prevention recommendations
        
        Respond in {lang} language. Be specific and actionable."""
        
        # Call Gemini with image
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": query},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64
                            }
                        }
                    ]
                }
            ],
            config={
                "system_instruction": system_prompt,
                "temperature": 0.3,
                "max_output_tokens": 2048
            }
        )
        
        return jsonify({
            "success": True,
            "analysis": response.text,
            "model": "gemini-2.5-flash"
        }), 200
        
    except Exception as e:
        print(f"Gemini Vision Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@gemini_bp.route("/gemini/farming-advice", methods=["POST"])
def farming_advice():
    """
    Get personalized farming advice based on user context
    """
    try:
        data = request.json
        
        # User context
        crop = data.get("crop", "general")
        location = data.get("location", "India")
        season = data.get("season", "current")
        land_size = data.get("land_size", "1 hectare")
        question = data.get("question", "")
        lang = data.get("lang", "English")
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
        
        if not client:
            return jsonify({"error": "Gemini API not configured"}), 500
        
        context_prompt = f"""You are an expert agricultural advisor.
        
        Farmer Context:
        - Crop: {crop}
        - Location: {location}
        - Season: {season}
        - Land Size: {land_size}
        
        Provide specific, actionable advice considering local conditions.
        Include costs and timelines when relevant.
        Respond in {lang} language."""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"role": "user", "parts": [{"text": question}]}],
            config={
                "system_instruction": context_prompt,
                "temperature": 0.5,
                "max_output_tokens": 2048
            }
        )
        
        return jsonify({
            "success": True,
            "advice": response.text,
            "model": "gemini-2.5-flash",
            "context": {"crop": crop, "location": location, "season": season}
        }), 200
        
    except Exception as e:
        print(f"Gemini Advice Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@gemini_bp.route("/gemini/translate", methods=["POST"])
def translate_text():
    """
    Translate agricultural text to local languages using Gemini
    """
    try:
        data = request.json
        text = data.get("text", "")
        target_lang = data.get("target_lang", "Hindi")
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        if not client:
            return jsonify({"error": "Gemini API not configured"}), 500
        
        prompt = f"""Translate the following agricultural text to {target_lang}.
        Maintain technical accuracy while using simple, farmer-friendly language.
        Preserve any specific crop names, chemical names, or technical terms.
        
        Text to translate:
        {text}"""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
            config={"temperature": 0.2, "max_output_tokens": 2048}
        )
        
        return jsonify({
            "success": True,
            "translated_text": response.text,
            "target_language": target_lang,
            "model": "gemini-2.5-flash"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@gemini_bp.route("/gemini/status", methods=["GET"])
def gemini_status():
    """Check Gemini API configuration status"""
    return jsonify({
        "configured": bool(GOOGLE_API_KEY and client),
        "model": "gemini-2.5-flash",
        "endpoints": [
            "/gemini/chat",
            "/gemini/analyze-image",
            "/gemini/farming-advice",
            "/gemini/translate"
        ],
        "contexts": list(SYSTEM_PROMPTS.keys()),
        "note": "Get API key at: https://aistudio.google.com/app/apikey"
    }), 200
