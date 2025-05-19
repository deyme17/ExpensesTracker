# server/app.py
from flask import Flask
from server.api.auth_routes import auth_bp
from server.api.transaction_routes import transactions_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(transactions_bp)

if __name__ == "__main__":
    app.run(debug=True)
