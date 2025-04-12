from flask import Flask, send_from_directory
from api import api, init_controller
import os

site_prefix = "" # "/rdb" #
api_prefix = "/api"
_N = len(site_prefix) + len(api_prefix)

app = Flask(__name__, static_folder='../frontend/dist')

# Initialize the connector
init_controller()

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
