from flask import Blueprint, jsonify, request
from flask_cors import CORS
import atexit

from rtm import TagStr, TagStrFull, Manager, Resource, TAG_SPLITTER
from rdb import SQLiteResourceConnector, SQLiteResource

api = Blueprint('api', __name__)
CORS(api)
tag_manager = manager = Manager()
connector: SQLiteResourceConnector = None

@api.route("/tags", defaults={'tag': ''}, methods=['GET']) # equal to `/tags/<empty>`
@api.route("/tags/", defaults={'tag': ''}, methods=['GET'])
@api.route("/tags/<string:tag>", methods=['GET']) # list-sub
def list_tags_of(tag: TagStrFull):
    return manager.get_tags_of(tag)

@api.route("/tags", methods=['POST']) # create
def create_tag():
    tag = request.json.get('tag')
    if not tag:
        return jsonify({'error': 'Tag is required'}), 400
    manager.add_tag(tag)
    return jsonify({'message': 'Tag created successfully'}), 201

@api.route("/resources", methods=['GET'])
def show_resource_list(): # order by added date
    tags = request.args.get('tags', '', type=str)
    if tags: # not empty tags, nor no-tags-key # /resources?tags=...
        t_resources = manager.filter_resources(tags.split(TAG_SPLITTER))
        resources = connector.get_resources_by_ids([t_res.res_id for t_res in t_resources])
        return jsonify({
            'resources': SQLiteResource.resources_to_meta_list(resources),
            'total_resources': len(resources),
            'items_per_page': 0,
        })
    else: # /resources, /resources?page=..., /resources?tags=<empty>
        ITEMS_PER_PAGE = 9
        page = request.args.get('page', 1, type=int)
        page = max(0, page-1)
        resources = connector.get_resources_by_page(page, ITEMS_PER_PAGE)
        return jsonify({
            'resources': SQLiteResource.resources_to_meta_list(resources),
            'total_resources': connector.total_resources,
            'items_per_page': ITEMS_PER_PAGE,
        })

@api.route("/resources/<string:resource>", methods=['GET'])
def show_resource(resource: str):
    res_id = int(resource)
    resource_obj = connector.get_resource(res_id)
    if not resource_obj:
        return jsonify({'error': 'Resource not found'}), 404
    return jsonify(resource_obj.to_detail_dict())

@api.route("/resources", methods=['POST'])
def add_resource_with_tags():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Resource name is required'}), 400
    
    tags = TAG_SPLITTER.join(data.get('tags', []))  # Optional tags string (tag1;;tag2;;tag3)
    resource = connector.new_resource(
        data['name'], tags,
        data.get('description', ''), data.get('link', ''), data.get('content', ''), data.get('type', '')
    )
    
    manager.add_resource(resource)
    return jsonify({'message': 'Resource created successfully'}), 201

def init_connector():
    from os import path
    db_path = path.join(path.dirname(__file__), '../storage/resources.db')
    global connector
    connector = SQLiteResourceConnector(manager, db_path)
    connector.load_resources()
    atexit.register(connector.close)

if __name__=="__main__":
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/api')
    init_connector()
    app.run(host="localhost", port="5428", debug=True)