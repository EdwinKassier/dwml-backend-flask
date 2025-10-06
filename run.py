"""This is the core of the api - BACKWARDS COMPATIBLE VERSION
creating a central point for blueprinted frameworks to flow through"""

import json
import os
from app import create_app

# Create app with backwards compatibility
app = create_app()

# PRESERVE: Exact same status endpoint
@app.route('/status', methods=['GET'])
def status():
    """Indicate the status of the api - EXACT SAME BEHAVIOR."""
    return (json.dumps({"message": 'DudeWheresMyLambo API Status : Running!'}),
            200, {"ContentType": "application/json"})


# PRESERVE: Exact same home endpoint
@app.route('/', methods=['GET'])
def home():
    """Welcome the user on a request to home - EXACT SAME BEHAVIOR."""
    return (json.dumps({"message": 'Welcome to the DudeWheresMyLambo API'}),
            200, {"ContentType": "application/json"})


# NEW: Add backwards-compatible production server support
def run_production_server():
    """Run production server with gunicorn if available."""
    try:
        import gunicorn.app.wsgiapp as wsgi
        wsgi.run()
    except ImportError:
        # Fallback to development server
        app.run(port=int(os.environ.get("PORT", 8080)), 
                host='0.0.0.0', 
                debug=False)  # FIXED: Disable debug in production


def run_development_server():
    """Run development server with enhanced features."""
    # NEW: Add development-specific configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(port=int(os.environ.get("PORT", 8080)), 
            host='0.0.0.0', 
            debug=debug_mode)


if __name__ == '__main__':
    # NEW: Environment-aware server selection
    environment = os.environ.get('FLASK_ENV', 'development')
    
    if environment == 'production':
        run_production_server()
    else:
        # PRESERVE: Existing development behavior
        run_development_server()