from flask import Flask, send_from_directory
from app import api, init_connector
import os

app = Flask(__name__, static_folder='../frontend/dist')

# Initialize the connector
init_connector()

# Register the API blueprint
app.register_blueprint(api, url_prefix='/api')

# Serve the frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
