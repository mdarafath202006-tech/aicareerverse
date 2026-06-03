"""AI CareerVerse — Application entry point"""
import os
from app import create_app, socketio

config = os.getenv("FLASK_ENV", "production")
config_map = {
    "development": "config.DevelopmentConfig",
    "testing":     "config.DevelopmentConfig",
    "production":  "config.ProductionConfig",
}

app = create_app(config_map.get(config, "config.ProductionConfig"))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = config == "development"
    socketio.run(app, host="0.0.0.0", port=port, debug=debug, use_reloader=debug)
