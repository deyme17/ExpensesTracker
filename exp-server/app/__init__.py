from .app import app

from app.routes.auth_routes import auth_bp, ping_bp
from app.routes.main_routes import api
from app.routes.webhook_routes import mono_webhook_bp
from app.routes.status import status_bp

app.register_blueprint(status_bp)
app.register_blueprint(api)
app.register_blueprint(auth_bp)
app.register_blueprint(ping_bp, url_prefix="/api")
app.register_blueprint(mono_webhook_bp)