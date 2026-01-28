from flask import Blueprint, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

huggingface_bp = Blueprint('huggingface_bp', __name__)

# Hugging Face API Configuration
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_INFERENCE_URL = "https://api-inference.huggingface.co/models"

# Agricultural models on Hugging Face
AGRI_MODELS = {
    # Text Generation Models (LLMs)
    "agriparam": {
        "id": "BharatGen/AgriParam",
        "type": "text-generation",
        "description": "India-centric agriculture LLM (English + Hindi)",
        "use_for": ["advisory", "policy", "general"]
    },
    "aksara": {
        "id": "cropinailab/aksara_v1",
        "type": "text-generation", 
        "description": "Crop lifecycle advisor (9 crops, India)",
        "use_for": ["crop_management", "disease", "soil"]
    },
    "agri-llama": {
        "id": "akhil-05/Agri-LLaMA-3-8B",
        "type": "text-generation",
        "description": "Agricultural fine-tuned Llama 3",
        "use_for": ["general", "advisory"]
    },
    
    # Image Classification Models
    "plant-disease": {
        "id": "ShrutikaDeshmukh/plant-disease-classification-model-finetuned",
        "type": "image-classification",
        "description": "Plant disease detection from leaf images",
        "use_for": ["disease_detection"]
    },
    "crop-disease": {
        "id": "linkanjarad/mobilenet_v2_1.0_224-finetuned-plantdisease",
        "type": "image-classification",
        "description": "MobileNetV2 plant disease classifier",
        "use_for": ["disease_detection"]
    },
    
    # Specialized Models
    "fertilizer": {
        "id": "DNgigi/FertiliserApplication",
        "type": "tabular-classification",
        "description": "Fertilizer requirement prediction",
        "use_for": ["fertilizer"]
    },
    "crop-recommend": {
        "id": "Novadotgg/Crop-recommendation",
        "type": "tabular-classification",
        "description": "Crop recommendation based on soil/weather",
        "use_for": ["crop_recommendation"]
    }
}

# Agricultural prompts for LLMs
AGRI_PROMPTS = {
    "disease": """You are an expert plant pathologist. Analyze the following query about plant disease and provide:
1. Disease identification
2. Symptoms to look for
3. Causes and spread pattern
4. Treatment (organic and chemical options)
5. Prevention measures

Query: {query}

Provide practical advice for Indian farmers.""",

    "advisory": """You are an expert agricultural advisor for Indian farmers. Provide practical, actionable advice on the following farming query:

Query: {query}

Include specific recommendations, costs if relevant, and timing considerations.""",

    "fertilizer": """You are a soil and fertilizer expert. Based on the following query, provide fertilizer recommendations:

Query: {query}

Include NPK ratios, application timing, quantity per acre, and organic alternatives.""",

    "crop_management": """You are a crop management specialist. Provide guidance on:

Query: {query}

Include planting tips, irrigation schedule, pest management, and harvest timing."""
}


@huggingface_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@huggingface_bp.route("/huggingface/chat", methods=["POST"])
def hf_chat():
    """
    Chat with agricultural LLMs on Hugging Face
    """
    try:
        data = request.json
        query = data.get("query", "")
        model = data.get("model", "agriparam")  # Use preset name
        context = data.get("context", "advisory")  # disease, advisory, fertilizer, crop_management
        lang = data.get("lang", "English")
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        if not HF_API_KEY:
            return jsonify({"error": "Hugging Face API key not configured"}), 500
        
        # Get model info
        model_info = AGRI_MODELS.get(model, AGRI_MODELS["agriparam"])
        model_id = model_info["id"]
        
        # Build prompt
        prompt_template = AGRI_PROMPTS.get(context, AGRI_PROMPTS["advisory"])
        prompt = prompt_template.format(query=query)
        
        if lang != "English":
            prompt += f"\n\nRespond in {lang} language."
        
        # Call Hugging Face Inference API
        response = requests.post(
            f"{HF_INFERENCE_URL}/{model_id}",
            headers={"Authorization": f"Bearer {HF_API_KEY}"},
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 1024,
                    "temperature": 0.7,
                    "do_sample": True,
                    "return_full_text": False
                }
            },
            timeout=120  # Models may need warmup time
        )
        
        if response.status_code == 503:
            # Model is loading
            return jsonify({
                "success": False,
                "loading": True,
                "message": "Model is loading, please try again in 20-30 seconds",
                "model": model_id
            }), 503
        
        response.raise_for_status()
        result = response.json()
        
        # Extract generated text
        if isinstance(result, list) and len(result) > 0:
            generated = result[0].get("generated_text", "")
        else:
            generated = str(result)
        
        return jsonify({
            "success": True,
            "response": generated,
            "model": model_id,
            "context": context
        }), 200
        
    except requests.exceptions.RequestException as e:
        print(f"HuggingFace API Error: {str(e)}")
        return jsonify({"error": f"HuggingFace API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@huggingface_bp.route("/huggingface/disease-detect", methods=["POST"])
def hf_disease_detect():
    """
    Detect plant diseases from images using HuggingFace vision models
    """
    try:
        data = request.json
        image_base64 = data.get("image")
        model = data.get("model", "plant-disease")
        
        if not image_base64:
            return jsonify({"error": "Image (base64) is required"}), 400
        
        if not HF_API_KEY:
            return jsonify({"error": "Hugging Face API key not configured"}), 500
        
        model_info = AGRI_MODELS.get(model, AGRI_MODELS["plant-disease"])
        model_id = model_info["id"]
        
        # Decode base64 image
        import base64
        image_bytes = base64.b64decode(image_base64)
        
        # Call image classification endpoint
        response = requests.post(
            f"{HF_INFERENCE_URL}/{model_id}",
            headers={"Authorization": f"Bearer {HF_API_KEY}"},
            data=image_bytes,
            timeout=60
        )
        
        if response.status_code == 503:
            return jsonify({
                "success": False,
                "loading": True,
                "message": "Model is loading, please try again in 20-30 seconds"
            }), 503
        
        response.raise_for_status()
        predictions = response.json()
        
        # Format results
        results = []
        for pred in predictions[:5]:  # Top 5 predictions
            results.append({
                "disease": pred.get("label", "Unknown"),
                "confidence": round(pred.get("score", 0) * 100, 2)
            })
        
        return jsonify({
            "success": True,
            "predictions": results,
            "top_disease": results[0] if results else None,
            "model": model_id
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@huggingface_bp.route("/huggingface/crop-recommend", methods=["POST"])
def hf_crop_recommend():
    """
    Get crop recommendations based on soil and weather conditions
    Uses the Crop-recommendation model
    """
    try:
        data = request.json
        
        # Soil and weather parameters
        nitrogen = data.get("nitrogen", 50)
        phosphorus = data.get("phosphorus", 50)
        potassium = data.get("potassium", 50)
        temperature = data.get("temperature", 25)
        humidity = data.get("humidity", 70)
        ph = data.get("ph", 6.5)
        rainfall = data.get("rainfall", 100)
        
        if not HF_API_KEY:
            # Return common recommendations without API
            recommendations = get_offline_crop_recommendation(
                nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall
            )
            return jsonify({
                "success": True,
                "recommendations": recommendations,
                "source": "offline_rules",
                "note": "Configure HUGGINGFACE_API_KEY for ML-based recommendations"
            }), 200
        
        # For tabular models, we'd need a different approach
        # Most HF crop models expect specific input format
        # Falling back to rule-based for now with API enhancement
        
        recommendations = get_offline_crop_recommendation(
            nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall
        )
        
        return jsonify({
            "success": True,
            "recommendations": recommendations,
            "input_params": {
                "N": nitrogen, "P": phosphorus, "K": potassium,
                "temp": temperature, "humidity": humidity,
                "ph": ph, "rainfall": rainfall
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_offline_crop_recommendation(n, p, k, temp, humidity, ph, rainfall):
    """
    Rule-based crop recommendations for offline fallback
    """
    recommendations = []
    
    # Rice
    if humidity > 70 and rainfall > 150 and temp > 20:
        recommendations.append({
            "crop": "Rice (धान)",
            "suitability": "High",
            "reason": "High humidity and rainfall ideal for paddy"
        })
    
    # Wheat
    if temp < 25 and rainfall < 100 and ph > 6:
        recommendations.append({
            "crop": "Wheat (गेहूं)",
            "suitability": "High",
            "reason": "Cool weather and moderate rainfall perfect for wheat"
        })
    
    # Cotton
    if temp > 25 and n > 40 and k > 40:
        recommendations.append({
            "crop": "Cotton (कपास)",
            "suitability": "Medium-High",
            "reason": "Warm climate with good N-K levels"
        })
    
    # Sugarcane
    if temp > 20 and humidity > 60 and rainfall > 100:
        recommendations.append({
            "crop": "Sugarcane (गन्ना)",
            "suitability": "High",
            "reason": "Tropical conditions with adequate water"
        })
    
    # Maize
    if temp > 18 and temp < 35 and n > 50:
        recommendations.append({
            "crop": "Maize (मक्का)",
            "suitability": "High",
            "reason": "Good nitrogen levels for corn"
        })
    
    # Pulses (general)
    if n < 40 and ph > 6 and ph < 7.5:
        recommendations.append({
            "crop": "Pulses (दाल)",
            "suitability": "Medium-High",
            "reason": "Pulses fix nitrogen, good for low-N soils"
        })
    
    # Vegetables (general)
    if p > 40 and k > 40 and ph > 5.5:
        recommendations.append({
            "crop": "Vegetables (सब्जियां)",
            "suitability": "High",
            "reason": "Good P-K levels for vegetable crops"
        })
    
    # Sort by suitability
    suitability_order = {"High": 0, "Medium-High": 1, "Medium": 2, "Low": 3}
    recommendations.sort(key=lambda x: suitability_order.get(x["suitability"], 5))
    
    return recommendations[:5]


@huggingface_bp.route("/huggingface/models", methods=["GET"])
def list_hf_models():
    """
    List available agricultural models
    """
    return jsonify({
        "success": True,
        "models": AGRI_MODELS,
        "categories": {
            "text_generation": ["agriparam", "aksara", "agri-llama"],
            "image_classification": ["plant-disease", "crop-disease"],
            "tabular": ["fertilizer", "crop-recommend"]
        }
    }), 200


@huggingface_bp.route("/huggingface/status", methods=["GET"])
def hf_status():
    """Check Hugging Face API configuration status"""
    return jsonify({
        "configured": bool(HF_API_KEY),
        "endpoints": [
            "/huggingface/chat",
            "/huggingface/disease-detect",
            "/huggingface/crop-recommend",
            "/huggingface/models"
        ],
        "recommended_models": {
            "chat": "agriparam (India-focused LLM)",
            "disease": "plant-disease (leaf image classifier)",
            "crops": "crop-recommend (soil-based)"
        },
        "note": "Get free API key at: https://huggingface.co/settings/tokens"
    }), 200
