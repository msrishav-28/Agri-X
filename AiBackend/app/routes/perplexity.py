from flask import Blueprint, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

perplexity_bp = Blueprint('perplexity_bp', __name__)
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

@perplexity_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@perplexity_bp.route("/perplexity/chat", methods=["POST"])
def perplexity_chat():
    """
    Agricultural Q&A with web search using Perplexity Sonar API
    """
    try:
        data = request.json
        query = data.get("query", "")
        lang = data.get("lang", "English")
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        if not PERPLEXITY_API_KEY:
            return jsonify({"error": "Perplexity API key not configured"}), 500
        
        # System prompt for agricultural context
        system_prompt = f"""You are an expert agricultural advisor for Indian farmers. 
        Provide accurate, practical advice on:
        - Crop management and best practices
        - Pest and disease control
        - Government schemes and subsidies
        - Market prices and trends
        - Weather-based farming recommendations
        
        Always cite your sources when providing information.
        Respond in {lang} language.
        Keep responses concise and actionable for farmers."""
        
        payload = {
            "model": "sonar",  # Perplexity's search-enabled model
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            "temperature": 0.2,
            "return_citations": True,
            "search_recency_filter": "month"  # Focus on recent information
        }
        
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        citations = result.get("citations", [])
        
        return jsonify({
            "success": True,
            "answer": answer,
            "citations": citations,
            "model": "perplexity-sonar"
        }), 200
        
    except requests.exceptions.RequestException as e:
        print(f"Perplexity API Error: {str(e)}")
        return jsonify({"error": "Error communicating with Perplexity API"}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500
