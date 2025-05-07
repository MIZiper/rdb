from flask import Blueprint, jsonify, request
from flask_cors import CORS
import atexit
import json

from rtm import TagStrFull, Manager, TAG_SPLITTER
from modules import RecordContentHandler
from rdb import SQLiteController

api = Blueprint('api', __name__)
CORS(api)
tag_manager = manager = Manager()
controller: SQLiteController = None

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
        resources = manager.filter_resources(tags.split(TAG_SPLITTER))
        records = controller.get_meta_records_by_ids([res.res_id for res in resources])
        return jsonify({
            'resources': [controller.to_meta_dict(rec) for rec in records],
            'total_resources': len(records),
            'items_per_page': 0,
        })
    else: # /resources, /resources?page=..., /resources?tags=<empty>
        ITEMS_PER_PAGE = 9
        page = request.args.get('page', 1, type=int)
        page = max(0, page-1)
        records = controller.get_meta_records_by_page(page, ITEMS_PER_PAGE)
        return jsonify({
            'resources': [controller.to_meta_dict(rec) for rec in records],
            'total_resources': controller.total_resources,
            'items_per_page': ITEMS_PER_PAGE,
        })

@api.route("/resources/<string:resource>", methods=['GET'])
def show_resource(resource: str):
    res_id = int(resource)
    record = controller.get_full_record_by_id(res_id)

    if not record:
        return jsonify({'error': 'Resource not found'}), 404
    
    handler = RecordContentHandler.get_handler(record.ModuleInfo)
    content = handler.to_client(record.Content)

    rec_dict = controller.to_detail_dict(record)
    rec_dict['content'] = content
    rec_dict['module'] = handler.module_name

    return jsonify(rec_dict)

@api.route("/resources", methods=['POST'])
def add_resource_with_tags():
    if request.content_type.startswith('multipart/form-data'):
        # Parse metadata from FormData
        metadata = request.form.get('metadata')
        if metadata:
            metadata = json.loads(metadata)
        else:
            return jsonify({'error': 'Metadata is required'}), 400

        client_content = request
    else:
        # Handle JSON payload
        metadata = request.json
        client_content = metadata.get('content', '')

    if not metadata or not metadata.get('title'):
        return jsonify({'error': 'Resource title is required'}), 400

    module_info = metadata.get('module', '')

    handler = RecordContentHandler.get_handler(module_info)
    db_content = handler.to_database(client_content)

    record = controller.new_resource(
        metadata['title'], metadata.get('tags', ''),
        metadata.get('description', ''), metadata.get('link', ''), db_content, module_info,
    )

    return jsonify({
        'message': 'Resource created successfully',
        'uuid': record.UUID,
    }), 201

def register_module_apis(api_blueprint):
    """Dynamically register APIs for all modules."""
    for handler_obj in RecordContentHandler._registry.values():
        # Dynamically call the register_api method of the handler object
        handler_obj.register_api(api_blueprint)

# Register module APIs dynamically
register_module_apis(api)

def init_controller():
    from os import path
    db_path = path.join(path.dirname(__file__), '../storage/resources.db')
    global controller
    controller = SQLiteController(manager, db_path)
    controller.load_resources()
    atexit.register(controller.close)

if __name__=="__main__":
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/api')
    init_controller()
    app.run(host="localhost", port="5428", debug=True)