from flask import Blueprint, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

alu_bp = Blueprint('alu_bp', __name__)

# Google ALU API Configuration
# Apply for access at: https://developers.google.com/earth-engine/datasets/alu
ALU_API_KEY = os.getenv("GOOGLE_ALU_API_KEY")
ALU_BASE_URL = "https://alu.googleapis.com/v1"  # Placeholder URL

@alu_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@alu_bp.route("/alu/crop-health", methods=["POST"])
def get_crop_health():
    """
    Get satellite-based crop health data for a field
    Uses NDVI and vegetation indices from ALU API
    """
    try:
        data = request.json
        
        # Field location (required)
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        
        if not latitude or not longitude:
            return jsonify({"error": "Latitude and longitude are required"}), 400
        
        if not ALU_API_KEY:
            # Return mock data for development/demo
            return jsonify({
                "success": True,
                "source": "mock",
                "message": "ALU API key not configured - showing demo data",
                "data": {
                    "location": {"lat": latitude, "lng": longitude},
                    "ndvi": 0.72,  # Normalized Difference Vegetation Index
                    "ndvi_status": "Healthy",
                    "crop_stress_index": 0.15,
                    "soil_moisture": 0.45,
                    "last_updated": "2026-01-27T10:00:00Z",
                    "recommendations": [
                        "Crop health is good based on satellite imagery",
                        "No signs of water stress detected",
                        "Continue current irrigation schedule"
                    ]
                }
            }), 200
        
        # Real API call when key is available
        payload = {
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "analysis_type": "crop_health",
            "include_ndvi": True,
            "include_moisture": True
        }
        
        headers = {
            "Authorization": f"Bearer {ALU_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{ALU_BASE_URL}/analyze/crop-health",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        return jsonify({
            "success": True,
            "source": "google_alu",
            "data": response.json()
        }), 200
        
    except requests.exceptions.RequestException as e:
        print(f"ALU API Error: {str(e)}")
        return jsonify({"error": "Error communicating with ALU API"}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@alu_bp.route("/alu/field-boundary", methods=["POST"])
def detect_field_boundary():
    """
    Detect agricultural field boundaries from satellite imagery
    Useful for land documentation and scheme eligibility
    """
    try:
        data = request.json
        
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        radius_meters = data.get("radius", 500)  # Search radius
        
        if not latitude or not longitude:
            return jsonify({"error": "Latitude and longitude are required"}), 400
        
        if not ALU_API_KEY:
            # Return mock data for development
            return jsonify({
                "success": True,
                "source": "mock",
                "message": "ALU API key not configured - showing demo data",
                "data": {
                    "detected_fields": 1,
                    "field_area_hectares": 2.5,
                    "field_area_acres": 6.18,
                    "boundary_coordinates": [
                        [longitude - 0.002, latitude - 0.002],
                        [longitude + 0.002, latitude - 0.002],
                        [longitude + 0.002, latitude + 0.002],
                        [longitude - 0.002, latitude + 0.002],
                        [longitude - 0.002, latitude - 0.002]  # Close polygon
                    ],
                    "confidence": 0.87,
                    "crop_type_detected": "Rice",
                    "last_updated": "2026-01-27T10:00:00Z"
                }
            }), 200
        
        # Real API call when key is available
        payload = {
            "center": {"latitude": latitude, "longitude": longitude},
            "radius_meters": radius_meters,
            "detect_crop_type": True
        }
        
        headers = {
            "Authorization": f"Bearer {ALU_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{ALU_BASE_URL}/detect/field-boundary",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        return jsonify({
            "success": True,
            "source": "google_alu",
            "data": response.json()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alu_bp.route("/alu/crop-classification", methods=["POST"])
def classify_crop():
    """
    Identify crop type growing in a field using satellite imagery
    """
    try:
        data = request.json
        
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        
        if not latitude or not longitude:
            return jsonify({"error": "Latitude and longitude are required"}), 400
        
        if not ALU_API_KEY:
            # Return mock data for development
            return jsonify({
                "success": True,
                "source": "mock",
                "message": "ALU API key not configured - showing demo data",
                "data": {
                    "location": {"lat": latitude, "lng": longitude},
                    "crop_predictions": [
                        {"crop": "Rice", "confidence": 0.85},
                        {"crop": "Wheat", "confidence": 0.08},
                        {"crop": "Maize", "confidence": 0.05},
                        {"crop": "Other", "confidence": 0.02}
                    ],
                    "primary_crop": "Rice",
                    "growth_stage": "Vegetative",
                    "estimated_sowing_date": "2025-11-15",
                    "estimated_harvest_date": "2026-03-20",
                    "last_updated": "2026-01-27T10:00:00Z"
                }
            }), 200
        
        # Real API call when key is available
        headers = {
            "Authorization": f"Bearer {ALU_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{ALU_BASE_URL}/classify/crop",
            headers=headers,
            json={"location": {"latitude": latitude, "longitude": longitude}},
            timeout=30
        )
        response.raise_for_status()
        
        return jsonify({
            "success": True,
            "source": "google_alu",
            "data": response.json()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alu_bp.route("/alu/yield-prediction", methods=["POST"])
def predict_yield():
    """
    Predict crop yield based on satellite data and historical patterns
    """
    try:
        data = request.json
        
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        crop_type = data.get("crop_type", "auto")  # Auto-detect or specify
        field_area_hectares = data.get("field_area", 1.0)
        
        if not latitude or not longitude:
            return jsonify({"error": "Latitude and longitude are required"}), 400
        
        if not ALU_API_KEY:
            # Return mock data for development
            return jsonify({
                "success": True,
                "source": "mock",
                "message": "ALU API key not configured - showing demo data",
                "data": {
                    "location": {"lat": latitude, "lng": longitude},
                    "crop_type": crop_type if crop_type != "auto" else "Rice",
                    "field_area_hectares": field_area_hectares,
                    "yield_prediction": {
                        "expected_yield_kg_per_hectare": 4200,
                        "expected_total_yield_kg": 4200 * field_area_hectares,
                        "confidence": 0.78,
                        "range": {
                            "low": 3800 * field_area_hectares,
                            "high": 4600 * field_area_hectares
                        }
                    },
                    "comparison": {
                        "district_average": 3900,
                        "state_average": 4100,
                        "national_average": 3800
                    },
                    "factors": {
                        "soil_condition": "Good",
                        "water_availability": "Adequate",
                        "weather_outlook": "Favorable"
                    },
                    "estimated_harvest_date": "2026-03-20",
                    "last_updated": "2026-01-27T10:00:00Z"
                }
            }), 200
        
        # Real API call when key is available
        headers = {
            "Authorization": f"Bearer {ALU_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{ALU_BASE_URL}/predict/yield",
            headers=headers,
            json={
                "location": {"latitude": latitude, "longitude": longitude},
                "crop_type": crop_type,
                "field_area_hectares": field_area_hectares
            },
            timeout=30
        )
        response.raise_for_status()
        
        return jsonify({
            "success": True,
            "source": "google_alu",
            "data": response.json()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@alu_bp.route("/alu/status", methods=["GET"])
def alu_status():
    """
    Check ALU API configuration status
    """
    return jsonify({
        "configured": bool(ALU_API_KEY),
        "endpoints": [
            "/alu/crop-health",
            "/alu/field-boundary",
            "/alu/crop-classification",
            "/alu/yield-prediction"
        ],
        "note": "Apply for Google ALU API access at: https://developers.google.com/earth-engine/datasets"
    }), 200
