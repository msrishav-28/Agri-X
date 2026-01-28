from flask import Blueprint, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

myscheme_bp = Blueprint('myscheme_bp', __name__)
MYSCHEME_API_KEY = os.getenv("MYSCHEME_API_KEY")

# API Setu base URL for myScheme
MYSCHEME_BASE_URL = "https://api.myscheme.gov.in"

@myscheme_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@myscheme_bp.route("/myscheme/search", methods=["POST"])
def search_schemes():
    """
    Search government schemes based on criteria
    """
    try:
        data = request.json
        
        # Search parameters
        params = {
            "schemeName": data.get("scheme_name", ""),
            "tags": data.get("tags", "agriculture"),  # Default to agriculture
            "age": data.get("age"),
            "isMinority": data.get("is_minority", False),
            "beneficiaryState": data.get("state"),
            "residence": data.get("residence"),  # rural/urban
            "isGovtEmployee": data.get("is_govt_employee", False)
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        headers = {
            "X-API-Key": MYSCHEME_API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{MYSCHEME_BASE_URL}/api/v1/schemes/search",
            headers=headers,
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            schemes = response.json()
            return jsonify({
                "success": True,
                "schemes": schemes,
                "count": len(schemes) if isinstance(schemes, list) else 0
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": f"API returned status {response.status_code}"
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        print(f"myScheme API Error: {str(e)}")
        return jsonify({"error": "Error communicating with myScheme API"}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@myscheme_bp.route("/myscheme/eligibility", methods=["POST"])
def check_eligibility():
    """
    Check scheme eligibility based on user profile
    """
    try:
        data = request.json
        
        # User profile for eligibility check
        user_profile = {
            "age": data.get("age"),
            "gender": data.get("gender"),
            "state": data.get("state"),
            "district": data.get("district"),
            "category": data.get("category"),  # General/SC/ST/OBC
            "isMinority": data.get("is_minority", False),
            "isDisabled": data.get("is_disabled", False),
            "isBPL": data.get("is_bpl", False),
            "isFarmer": data.get("is_farmer", True),  # Default True for AgriX
            "landHolding": data.get("land_holding"),  # in acres
            "annualIncome": data.get("annual_income"),
            "occupation": data.get("occupation", "Farmer")
        }
        
        headers = {
            "X-API-Key": MYSCHEME_API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{MYSCHEME_BASE_URL}/api/v1/eligibility/check",
            headers=headers,
            json=user_profile,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                "success": True,
                "eligible_schemes": result.get("schemes", []),
                "total_schemes": result.get("total", 0)
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": f"API returned status {response.status_code}"
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        print(f"myScheme Eligibility API Error: {str(e)}")
        return jsonify({"error": "Error checking eligibility"}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@myscheme_bp.route("/myscheme/agriculture", methods=["GET"])
def get_agriculture_schemes():
    """
    Get all agriculture-related schemes (cached/fallback response)
    """
    # Fallback data for common agriculture schemes
    agriculture_schemes = [
        {
            "name": "PM-KISAN",
            "full_name": "Pradhan Mantri Kisan Samman Nidhi",
            "benefit": "₹6,000 per year in 3 installments",
            "eligibility": "All landholding farmers",
            "link": "https://pmkisan.gov.in"
        },
        {
            "name": "PMFBY",
            "full_name": "Pradhan Mantri Fasal Bima Yojana",
            "benefit": "Crop insurance at subsidized premium",
            "eligibility": "All farmers growing notified crops",
            "link": "https://pmfby.gov.in"
        },
        {
            "name": "KCC",
            "full_name": "Kisan Credit Card",
            "benefit": "Credit up to ₹3 lakh at 4% interest",
            "eligibility": "All farmers, fishermen, animal husbandry farmers",
            "link": "https://www.pmkisan.gov.in/kcc"
        },
        {
            "name": "PKVY",
            "full_name": "Paramparagat Krishi Vikas Yojana",
            "benefit": "₹50,000/ha over 3 years for organic farming",
            "eligibility": "Farmers willing to adopt organic farming",
            "link": "https://pgsindia-ncof.gov.in"
        },
        {
            "name": "e-NAM",
            "full_name": "Electronic National Agriculture Market",
            "benefit": "Online trading platform for agricultural commodities",
            "eligibility": "All farmers and traders",
            "link": "https://enam.gov.in"
        }
    ]
    
    return jsonify({
        "success": True,
        "schemes": agriculture_schemes,
        "source": "cached",
        "note": "For personalized eligibility, use /myscheme/eligibility endpoint"
    }), 200
