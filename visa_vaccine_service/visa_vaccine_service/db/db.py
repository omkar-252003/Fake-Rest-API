import json
import os
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Absolute path to JSON database
DB_PATH = os.path.join(os.path.dirname(__file__), "database.json")

def load_database():
    """Loads travel service data from JSON."""
    try:
        with open(DB_PATH, "r") as file:
            data = json.load(file)
            logger.info("Database loaded successfully.")
            return data
    except FileNotFoundError:
        logger.error(f"Database file not found at {DB_PATH}")
        return {}

# Load data at startup
db_data = load_database()
