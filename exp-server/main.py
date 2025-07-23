from app.app import app
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)