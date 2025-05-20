from flask import Flask
from flask_cors import CORS
from server.api.endpoints import api

def create_app():
    app = Flask(__name__)
    CORS(app)  # дозволити запити з клієнта (Kivy, Postman тощо)
    app.register_blueprint(api)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
