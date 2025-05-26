from server.api.auth_routes import auth_bp
from flask import Flask
from flask_cors import CORS
from server.api.endpoints import api
from server.api.base import ping_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api)
    app.register_blueprint(auth_bp) 
    app.register_blueprint(ping_bp, url_prefix="/api")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)