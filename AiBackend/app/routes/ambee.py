from flask import Blueprint, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

ambee_bp = Blueprint('ambee_bp', __name__)

# Ambee API Configuration
AMBEE_API_KEY = os.getenv("AMBEE_API_KEY")
AMBEE_BASE_URL = "https://api.ambeedata.com"

@ambee_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


def get_ambee_headers():
    return {
        "x-api-key": AMBEE_API_KEY,
        "Content-Type": "application/json"
    }


# ============================================
# WEATHER API - Real-time weather for farming
# ============================================

@ambee_bp.route("/ambee/weather/latest", methods=["POST"])
def get_weather_latest():
    """
    Get real-time hyperlocal weather data (500m resolution)
    Useful for: irrigation scheduling, spraying decisions, harvest planning
    """
    try:
        data = request.json
        lat = data.get("latitude")
        lng = data.get("longitude")
        
        if not lat or not lng:
            return jsonify({"error": "Latitude and longitude required"}), 400
        
        if not AMBEE_API_KEY:
            return jsonify({"error": "Ambee API key not configured"}), 500
        
        response = requests.get(
            f"{AMBEE_BASE_URL}/weather/latest/by-lat-lng",
            headers=get_ambee_headers(),
            params={"lat": lat, "lng": lng},
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        return jsonify({
            "success": True,
            "source": "ambee",
            "data": result.get("data", {}),
            "farming_insights": generate_weather_insights(result.get("data", {}))
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ambee_bp.route("/ambee/weather/forecast", methods=["POST"])
def get_weather_forecast():
    """
    Get weather forecast for planning farming activities
    """
    try:
        data = request.json
        lat = data.get("latitude")
        lng = data.get("longitude")
        
        if not AMBEE_API_KEY:
            return jsonify({"error": "Ambee API key not configured"}), 500
        
        response = requests.get(
            f"{AMBEE_BASE_URL}/weather/forecast/by-lat-lng",
            headers=get_ambee_headers(),
            params={"lat": lat, "lng": lng},
            timeout=30
        )
        response.raise_for_status()
        
        return jsonify({
            "success": True,
            "source": "ambee",
            "data": response.json().get("data", {})
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# SOIL API - Soil moisture & temperature
# ============================================

@ambee_bp.route("/ambee/soil", methods=["POST"])
def get_soil_data():
    """
    Get soil moisture and temperature data
    Useful for: irrigation decisions, planting timing, crop health
    """
    try:
        data = request.json
        lat = data.get("latitude")
        lng = data.get("longitude")
        
        if not lat or not lng:
            return jsonify({"error": "Latitude and longitude required"}), 400
        
        if not AMBEE_API_KEY:
            return jsonify({"error": "Ambee API key not configured"}), 500
        
        response = requests.get(
            f"{AMBEE_BASE_URL}/soil/latest/by-lat-lng",
            headers=get_ambee_headers(),
            params={"lat": lat, "lng": lng},
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        return jsonify({
            "success": True,
            "source": "ambee",
            "data": result.get("data", {}),
            "irrigation_recommendation": generate_irrigation_advice(result.get("data", {}))
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# AIR QUALITY API - Spraying decisions
# ============================================

@ambee_bp.route("/ambee/air-quality", methods=["POST"])
def get_air_quality():
    """
    Get air quality data (AQI, pollutants)
    Useful for: pesticide spraying timing (avoid drift in bad air)
    """
    try:
        data = request.json
        lat = data.get("latitude")
        lng = data.get("longitude")
        
        if not AMBEE_API_KEY:
            return jsonify({"error": "Ambee API key not configured"}), 500
        
        response = requests.get(
            f"{AMBEE_BASE_URL}/latest/by-lat-lng",
            headers=get_ambee_headers(),
            params={"lat": lat, "lng": lng},
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        aqi = result.get("stations", [{}])[0].get("AQI", 0) if result.get("stations") else 0
        
        return jsonify({
            "success": True,
            "source": "ambee",
            "data": result,
            "aqi": aqi,
            "spray_recommendation": "Good for spraying" if aqi < 100 else "Avoid spraying - poor air quality"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# POLLEN API - Crop & worker health
# ============================================

@ambee_bp.route("/ambee/pollen", methods=["POST"])
def get_pollen_data():
    """
    Get pollen count data
    Useful for: crop pollination timing, worker allergy alerts
    """
    try:
        data = request.json
        lat = data.get("latitude")
        lng = data.get("longitude")
        
        if not AMBEE_API_KEY:
            return jsonify({"error": "Ambee API key not configured"}), 500
        
        response = requests.get(
            f"{AMBEE_BASE_URL}/latest/pollen/by-lat-lng",
            headers=get_ambee_headers(),
            params={"lat": lat, "lng": lng},
            timeout=30
        )
        response.raise_for_status()
        
        return jsonify({
            "success": True,
            "source": "ambee",
            "data": response.json().get("data", [])
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# WILDFIRE API - Crop protection alerts
# ============================================

@ambee_bp.route("/ambee/fire", methods=["POST"])
def get_fire_data():
    """
    Get wildfire alerts for the region
    Useful for: crop protection, evacuation planning, smoke alerts
    """
    try:
        data = request.json
        lat = data.get("latitude")
        lng = data.get("longitude")
        
        if not AMBEE_API_KEY:
            return jsonify({"error": "Ambee API key not configured"}), 500
        
        response = requests.get(
            f"{AMBEE_BASE_URL}/fire/latest/by-lat-lng",
            headers=get_ambee_headers(),
            params={"lat": lat, "lng": lng},
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        fires = result.get("data", [])
        
        return jsonify({
            "success": True,
            "source": "ambee",
            "fires_nearby": len(fires),
            "data": fires,
            "alert_level": "High" if len(fires) > 0 else "None"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# NATURAL DISASTER API - Weather warnings
# ============================================

@ambee_bp.route("/ambee/disasters", methods=["POST"])
def get_disaster_alerts():
    """
    Get natural disaster alerts (floods, cyclones, etc.)
    Useful for: crop protection, harvest timing, safety alerts
    """
    try:
        data = request.json
        lat = data.get("latitude")
        lng = data.get("longitude")
        
        if not AMBEE_API_KEY:
            return jsonify({"error": "Ambee API key not configured"}), 500
        
        response = requests.get(
            f"{AMBEE_BASE_URL}/disasters/latest/by-lat-lng",
            headers=get_ambee_headers(),
            params={"lat": lat, "lng": lng},
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        events = result.get("data", [])
        
        return jsonify({
            "success": True,
            "source": "ambee",
            "active_alerts": len(events),
            "data": events
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# COMBINED FARMING DASHBOARD
# ============================================

@ambee_bp.route("/ambee/farming-dashboard", methods=["POST"])
def get_farming_dashboard():
    """
    Get all environmental data for farming in one call
    Perfect for AgriX home screen dashboard
    """
    try:
        data = request.json
        lat = data.get("latitude")
        lng = data.get("longitude")
        
        if not lat or not lng:
            return jsonify({"error": "Latitude and longitude required"}), 400
        
        if not AMBEE_API_KEY:
            return jsonify({"error": "Ambee API key not configured"}), 500
        
        headers = get_ambee_headers()
        params = {"lat": lat, "lng": lng}
        
        # Fetch all data in parallel (simplified sequential for reliability)
        dashboard = {
            "location": {"lat": lat, "lng": lng},
            "weather": None,
            "soil": None,
            "air_quality": None,
            "alerts": []
        }
        
        # Weather
        try:
            weather_resp = requests.get(
                f"{AMBEE_BASE_URL}/weather/latest/by-lat-lng",
                headers=headers, params=params, timeout=10
            )
            if weather_resp.status_code == 200:
                dashboard["weather"] = weather_resp.json().get("data", {})
        except:
            pass
        
        # Soil
        try:
            soil_resp = requests.get(
                f"{AMBEE_BASE_URL}/soil/latest/by-lat-lng",
                headers=headers, params=params, timeout=10
            )
            if soil_resp.status_code == 200:
                dashboard["soil"] = soil_resp.json().get("data", {})
        except:
            pass
        
        # Air Quality
        try:
            aqi_resp = requests.get(
                f"{AMBEE_BASE_URL}/latest/by-lat-lng",
                headers=headers, params=params, timeout=10
            )
            if aqi_resp.status_code == 200:
                dashboard["air_quality"] = aqi_resp.json()
        except:
            pass
        
        # Fire alerts
        try:
            fire_resp = requests.get(
                f"{AMBEE_BASE_URL}/fire/latest/by-lat-lng",
                headers=headers, params=params, timeout=10
            )
            if fire_resp.status_code == 200:
                fires = fire_resp.json().get("data", [])
                if fires:
                    dashboard["alerts"].append({
                        "type": "fire",
                        "count": len(fires),
                        "severity": "high"
                    })
        except:
            pass
        
        # Generate farming insights
        dashboard["farming_insights"] = generate_farming_insights(dashboard)
        
        return jsonify({
            "success": True,
            "source": "ambee",
            "dashboard": dashboard
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_weather_insights(weather_data):
    """Generate farming-specific insights from weather data"""
    insights = []
    
    if not weather_data:
        return insights
    
    temp = weather_data.get("temperature", 0)
    humidity = weather_data.get("humidity", 0)
    wind_speed = weather_data.get("windSpeed", 0)
    
    # Temperature insights
    if temp > 35:
        insights.append("🌡️ High temperature - increase irrigation frequency")
    elif temp < 10:
        insights.append("❄️ Cold weather - protect frost-sensitive crops")
    
    # Humidity insights
    if humidity > 80:
        insights.append("💧 High humidity - watch for fungal diseases")
    elif humidity < 30:
        insights.append("🏜️ Low humidity - crops may need extra water")
    
    # Wind insights
    if wind_speed > 20:
        insights.append("💨 High winds - avoid pesticide spraying")
    
    return insights


def generate_irrigation_advice(soil_data):
    """Generate irrigation recommendations from soil data"""
    if not soil_data:
        return "Unable to determine - soil data unavailable"
    
    moisture = soil_data.get("soil_moisture", 50)
    temp = soil_data.get("soil_temperature", 25)
    
    if moisture < 20:
        return "🚨 Critical: Irrigate immediately - soil is very dry"
    elif moisture < 40:
        return "💧 Recommended: Irrigate within 24 hours"
    elif moisture > 80:
        return "⏸️ Hold irrigation - soil is adequately moist"
    else:
        return "✅ Soil moisture is optimal - maintain current schedule"


def generate_farming_insights(dashboard):
    """Generate comprehensive farming insights from all data"""
    insights = []
    
    # Weather-based insights
    weather = dashboard.get("weather", {})
    if weather:
        insights.extend(generate_weather_insights(weather))
    
    # Soil-based insights
    soil = dashboard.get("soil", {})
    if soil:
        irrigation = generate_irrigation_advice(soil)
        insights.append(irrigation)
    
    # Alert-based insights
    alerts = dashboard.get("alerts", [])
    for alert in alerts:
        if alert.get("type") == "fire":
            insights.append("🔥 Wildfire detected nearby - take precautions")
    
    return insights if insights else ["✅ Conditions look good for farming activities"]


@ambee_bp.route("/ambee/status", methods=["GET"])
def ambee_status():
    """Check Ambee API configuration status"""
    return jsonify({
        "configured": bool(AMBEE_API_KEY),
        "endpoints": [
            "/ambee/weather/latest",
            "/ambee/weather/forecast",
            "/ambee/soil",
            "/ambee/air-quality",
            "/ambee/pollen",
            "/ambee/fire",
            "/ambee/disasters",
            "/ambee/farming-dashboard"
        ],
        "note": "Get your API key at: https://api-dashboard.getambee.com"
    }), 200
