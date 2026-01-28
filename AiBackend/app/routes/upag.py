from flask import Blueprint, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

upag_bp = Blueprint('upag_bp', __name__)

# UPAg API Configuration
UPAG_BASE_URL = "https://data.upag.gov.in/v1/upag/api-data-share"
UPAG_USERNAME = os.getenv("UPAG_USERNAME")
UPAG_PASSWORD = os.getenv("UPAG_PASSWORD")

# Token cache (in production, use Redis or similar)
_token_cache = {"access_token": None}


@upag_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


def get_upag_token():
    """
    Get OAuth2 token from UPAg API
    """
    if _token_cache["access_token"]:
        return _token_cache["access_token"]
    
    try:
        response = requests.post(
            f"{UPAG_BASE_URL}/login",
            data={
                "username": UPAG_USERNAME,
                "password": UPAG_PASSWORD,
                "grant_type": "password"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            _token_cache["access_token"] = result.get("access_token")
            return _token_cache["access_token"]
        else:
            print(f"UPAg login failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"UPAg login error: {str(e)}")
        return None


@upag_bp.route("/upag/login", methods=["POST"])
def upag_login():
    """
    Authenticate with UPAg API and get access token
    """
    token = get_upag_token()
    if token:
        return jsonify({"success": True, "message": "Authenticated successfully"}), 200
    else:
        return jsonify({"success": False, "error": "Authentication failed"}), 401


@upag_bp.route("/upag/sources", methods=["GET"])
def get_allowed_sources():
    """
    Get list of available data sources
    """
    token = get_upag_token()
    if not token:
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        response = requests.get(
            f"{UPAG_BASE_URL}/sources/user-allowed-sources",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        elif response.status_code == 401:
            # Token expired, clear cache and retry
            _token_cache["access_token"] = None
            return jsonify({"error": "Token expired, please retry"}), 401
        else:
            return jsonify({"error": f"API returned {response.status_code}"}), response.status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@upag_bp.route("/upag/data/<source_name>", methods=["POST"])
def get_source_data(source_name):
    """
    Fetch data from a specific UPAg source
    
    Available sources:
    - dafw_state: State-level crop data (Area, Production, Yield)
    - dafw_district: District-level crop data
    - mncfc: MNCFC crop forecasts
    - agmarknet: Mandi prices
    - enam: e-NAM trading data
    - doca: Retail/wholesale prices
    - fci_stock: FCI grain stocks
    - fci_procurement: FCI procurement data
    - horticulture: Horticulture data
    """
    token = get_upag_token()
    if not token:
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        data = request.json
        
        # Build source input object based on source type
        source_input = {
            "limit": data.get("limit", 100),
            "offset": data.get("offset", 0),
            "source_name": source_name,
            "year": data.get("year", ["2023"])
        }
        
        # Add optional parameters based on source type
        if source_name in ["dafw_state", "mncfc", "ieg", "nsso", "cwwg", "pmfby_ay", "trs", "state_reported", "farmers_survey"]:
            source_input["location_granularity"] = data.get("location_granularity", "state")
        
        if source_name in ["dafw_state", "dafw_district", "dcs"]:
            source_input["season"] = data.get("season", ["kharif"])
        
        if source_name == "dafw_district":
            source_input["location_granularity"] = "district"
        
        if source_name == "dcs":
            source_input["location_granularity"] = "village"
            source_input["district"] = data.get("district", [])
            source_input["cropkey"] = data.get("cropkey", ["1"])
        
        if source_name == "dgcis":
            source_input["HsCode"] = data.get("hs_code", [])
            source_input["export_import_type"] = data.get("trade_type", ["import"])
        
        if source_name == "ncdex":
            source_input["date"] = data.get("date", ["2023-11-16"])
            del source_input["year"]
        
        payload = {"source_input_object": source_input}
        
        response = requests.post(
            f"{UPAG_BASE_URL}/sources/{source_name}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                "success": True,
                "source": source_name,
                "totalRecords": result.get("totalRecords", 0),
                "data": result.get("data", [])
            }), 200
        elif response.status_code == 401:
            _token_cache["access_token"] = None
            return jsonify({"error": "Token expired, please retry"}), 401
        else:
            return jsonify({
                "success": False,
                "error": f"API returned {response.status_code}",
                "details": response.text
            }), response.status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@upag_bp.route("/upag/crop-prices", methods=["POST"])
def get_crop_prices():
    """
    Convenience endpoint to get mandi prices (agmarknet data)
    """
    data = request.json or {}
    data["source_name"] = "agmarknet"
    request.json = data
    return get_source_data("agmarknet")


@upag_bp.route("/upag/crop-production", methods=["POST"])
def get_crop_production():
    """
    Convenience endpoint to get crop production data (dafw_state)
    """
    data = request.json or {}
    return get_source_data("dafw_state")
