from server.api.auth_routes import auth_bp, ping_bp
from server.api.main_routes import api
from server.api.webhook_routes import mono_webhook_bp

from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api)
    app.register_blueprint(auth_bp) 
    app.register_blueprint(ping_bp, url_prefix="/api")
    app.register_blueprint(mono_webhook_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
