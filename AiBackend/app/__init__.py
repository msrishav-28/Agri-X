from flask import Flask, jsonify
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Track loaded blueprints for status endpoint
    app.config['LOADED_BLUEPRINTS'] = []
    app.config['FAILED_BLUEPRINTS'] = []

    # ============================================
    # CORE ROUTES (Always required)
    # ============================================
    core_blueprints = [
        ('app.routes.govscheme', 'govscheme_bp'),
        ('app.routes.translate', 'translate_bp'),
        ('app.routes.plant_disease', 'plant_disease_bp'),
        ('app.routes.postharvest', 'postharvest_bp'),
        ('app.routes.agri_advisory', 'agri_advisory_bp'),
        ('app.routes.fertilizer', 'fertilizer_bp'),
        ('app.routes.market', 'weather_market_bp'),
        ('app.routes.crop_suggestion', 'crop_suggestion_bp'),
        ('app.routes.crop_calendar', 'crop_calendar_bp'),
        ('app.routes.water_management', 'water_management_bp'),
    ]
    
    # ============================================
    # EXTERNAL API INTEGRATIONS (Optional - with fallbacks)
    # ============================================
    external_blueprints = [
        ('app.routes.gemini', 'gemini_bp'),           # Primary AI
        ('app.routes.openrouter', 'openrouter_bp'),   # Fallback AI (300+ models)
        ('app.routes.huggingface', 'huggingface_bp'), # Fallback AI (AgriParam)
        ('app.routes.perplexity', 'perplexity_bp'),   # Web search AI
        ('app.routes.ambee', 'ambee_bp'),             # Weather/Soil data
        ('app.routes.myscheme', 'myscheme_bp'),       # Govt schemes
        ('app.routes.upag', 'upag_bp'),               # Agri statistics
        ('app.routes.alu', 'alu_bp'),                 # Satellite imagery
    ]
    
    def safe_register_blueprint(module_path, bp_name):
        """Safely register a blueprint with fallback handling"""
        try:
            module = __import__(module_path, fromlist=[bp_name])
            blueprint = getattr(module, bp_name)
            app.register_blueprint(blueprint)
            app.config['LOADED_BLUEPRINTS'].append(bp_name)
            return True
        except ImportError as e:
            print(f"⚠️ Warning: Could not import {module_path}: {e}")
            app.config['FAILED_BLUEPRINTS'].append({
                'name': bp_name,
                'error': str(e),
                'type': 'import_error'
            })
            return False
        except Exception as e:
            print(f"⚠️ Warning: Error registering {bp_name}: {e}")
            app.config['FAILED_BLUEPRINTS'].append({
                'name': bp_name,
                'error': str(e),
                'type': 'registration_error'
            })
            return False
    
    # Register core blueprints (required)
    print("\n📦 Loading Core Routes...")
    for module_path, bp_name in core_blueprints:
        if safe_register_blueprint(module_path, bp_name):
            print(f"  ✅ {bp_name}")
        else:
            print(f"  ❌ {bp_name} (FAILED)")
    
    # Register external API blueprints (optional - app works without them)
    print("\n🔌 Loading External API Integrations...")
    for module_path, bp_name in external_blueprints:
        if safe_register_blueprint(module_path, bp_name):
            print(f"  ✅ {bp_name}")
        else:
            print(f"  ⚠️ {bp_name} (skipped)")
    
    # ============================================
    # STATUS & HEALTH CHECK ENDPOINTS
    # ============================================
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify({
            "status": "healthy",
            "service": "AgriX AI Backend",
            "version": "2.0.0"
        }), 200
    
    @app.route('/api/status', methods=['GET'])
    def api_status():
        """Detailed API status with all loaded/failed blueprints"""
        # Check API key configuration
        api_keys = {
            "GROQ_API_KEY": bool(os.getenv("GROQ_API_KEY")),
            "GOOGLE_API_KEY": bool(os.getenv("GOOGLE_API_KEY")),
            "PERPLEXITY_API_KEY": bool(os.getenv("PERPLEXITY_API_KEY")),
            "AMBEE_API_KEY": bool(os.getenv("AMBEE_API_KEY")),
            "OPENROUTER_API_KEY": bool(os.getenv("OPENROUTER_API_KEY")),
            "HUGGINGFACE_API_KEY": bool(os.getenv("HUGGINGFACE_API_KEY")),
            "MYSCHEME_API_KEY": bool(os.getenv("MYSCHEME_API_KEY")),
            "UPAG_USERNAME": bool(os.getenv("UPAG_USERNAME")),
            "GOOGLE_ALU_API_KEY": bool(os.getenv("GOOGLE_ALU_API_KEY")),
        }
        
        configured_keys = sum(1 for v in api_keys.values() if v)
        
        return jsonify({
            "status": "running",
            "service": "AgriX AI Backend",
            "version": "2.0.0",
            "blueprints": {
                "loaded": app.config['LOADED_BLUEPRINTS'],
                "failed": app.config['FAILED_BLUEPRINTS'],
                "total_loaded": len(app.config['LOADED_BLUEPRINTS']),
                "total_failed": len(app.config['FAILED_BLUEPRINTS'])
            },
            "api_keys": {
                "configured": configured_keys,
                "total": len(api_keys),
                "details": api_keys
            },
            "ai_providers": {
                "primary": "gemini" if api_keys["GOOGLE_API_KEY"] else None,
                "fallback_1": "openrouter" if api_keys["OPENROUTER_API_KEY"] else None,
                "fallback_2": "huggingface" if api_keys["HUGGINGFACE_API_KEY"] else None,
                "fallback_3": "groq" if api_keys["GROQ_API_KEY"] else None,
            }
        }), 200
    
    @app.route('/api/ai-fallback', methods=['POST'])
    def ai_with_fallback():
        """
        Unified AI endpoint with automatic fallback
        Tries: Gemini -> OpenRouter -> HuggingFace -> Groq
        """
        from flask import request
        import requests as req
        
        data = request.json or {}
        message = data.get("message", "")
        context = data.get("context", "advisory")
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        providers = []
        
        # Try Gemini first
        if os.getenv("GOOGLE_API_KEY"):
            providers.append(("gemini", "/gemini/chat"))
        
        # Try OpenRouter
        if os.getenv("OPENROUTER_API_KEY"):
            providers.append(("openrouter", "/openrouter/chat"))
        
        # Try HuggingFace
        if os.getenv("HUGGINGFACE_API_KEY"):
            providers.append(("huggingface", "/huggingface/chat"))
        
        # Try internal endpoints
        for provider_name, endpoint in providers:
            try:
                # Make internal request
                with app.test_client() as client:
                    if provider_name == "huggingface":
                        resp = client.post(endpoint, json={"query": message, "context": context})
                    else:
                        resp = client.post(endpoint, json={"message": message, "context": context})
                    
                    if resp.status_code == 200:
                        result = resp.get_json()
                        result["provider"] = provider_name
                        return jsonify(result), 200
            except Exception as e:
                print(f"Fallback: {provider_name} failed: {e}")
                continue
        
        return jsonify({
            "error": "All AI providers failed",
            "tried": [p[0] for p in providers]
        }), 503
    
    print(f"\n✅ AgriX Backend Ready!")
    print(f"   Loaded: {len(app.config['LOADED_BLUEPRINTS'])} routes")
    print(f"   Failed: {len(app.config['FAILED_BLUEPRINTS'])} routes\n")
    
    return app
