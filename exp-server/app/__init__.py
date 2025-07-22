from .app import app

from app.api.auth_routes import auth_bp, ping_bp
from app.api.main_routes import api
from app.api.webhook_routes import mono_webhook_bp

app.register_blueprint(api)
app.register_blueprint(auth_bp)
app.register_blueprint(ping_bp, url_prefix="/api")
app.register_blueprint(mono_webhook_bp)