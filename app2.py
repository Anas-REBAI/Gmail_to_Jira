from flask import Flask
from utils.process import start_background_task, stop_background_task
from config.settings import APP_HOST, APP_PORT

# Flask application
app = Flask(__name__)

# Main execution
if __name__ == "__main__":
    # Start the background task
    start_background_task()

    try:
        app.run(host=APP_HOST, port=APP_PORT)
    finally:
        # Ensure background task is stopped gracefully
        stop_background_task()
