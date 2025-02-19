from flask import Flask, jsonify, request
from flask_cors import CORS
import atexit

from rtm import TagStr, TagStrFull, Manager, Resource, TAG_SPLITTER
from rdb import SQLiteResourceConnector

app = Flask(__name__)
CORS(app)
tag_manager = manager = Manager()
connector: SQLiteResourceConnector = None



@app.route("/tags", defaults={'tag': ''}, methods=['GET']) # equal to `/tags/<empty>`
@app.route("/tags/", defaults={'tag': ''}, methods=['GET'])
@app.route("/tags/<string:tag>", methods=['GET']) # list-sub
def list_tags_of(tag: TagStrFull):
    return manager.get_tags_of(tag)

@app.route("/tags", methods=['POST']) # create
def create_tag():
    tag = request.json.get('tag')
    if not tag:
        return jsonify({'error': 'Tag is required'}), 400
    manager.add_tag(tag)
    return jsonify({'message': 'Tag created successfully'}), 201

@app.route("/resources", methods=['GET'])
def show_resource_list(): # order by added date
    tags = request.args.get('tags', '', type=str)
    if tags: # not empty tags, nor no-tags-key # /resources?tags=...
        t_resources = manager.filter_resources(tags.split(TAG_SPLITTER))
        resources = connector.get_resources_by_ids([str(t_res.res_id) for t_res in t_resources])
        return jsonify({
            'resources': [res.to_dict() for res in resources],
            'total_resources': len(resources),
            'items_per_page': 0,
        })
    else: # /resources, /resources?page=..., /resources?tags=<empty>
        ITEMS_PER_PAGE = 9
        page = request.args.get('page', 1, type=int)
        page = max(0, page-1)
        resources = connector.get_resources_by_page(page, ITEMS_PER_PAGE)
        return jsonify({
            'resources': [res.to_dict() for res in resources],
            'total_resources': connector.total_resources,
            'items_per_page': ITEMS_PER_PAGE,
        })

@app.route("/resources/<string:resource>", methods=['GET'])
def show_resource(resource: str):
    res_id = int(resource)
    resource_obj = connector.get_resource(res_id)
    if not resource_obj:
        return jsonify({'error': 'Resource not found'}), 404
    return jsonify(resource_obj.to_dict())

@app.route("/resources", methods=['POST'])
def add_resource_with_tags():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Resource name is required'}), 400
    
    tags = data.get('tags', '')  # Optional tags string (tag1;;tag2;;tag3)
    resource = connector.new_resource(data['name'], tags)
    
    manager.add_resource(resource)
    return jsonify({'message': 'Resource created successfully'}), 201



if __name__=="__main__":
    from os import path
    import random

    db_path = path.join(path.dirname(__file__), '../storage/resources.db')
    if not path.exists(db_path):
        connector = SQLiteResourceConnector(manager, db_path)
        tags = [
            'cultivation','cultivation:ball','cultivation:apple','conscience','conscience:fry','conscience:fry:tend','conscience:nest',
            'build','build:disappoint','build:disappoint:tighten','build:disappoint:tighten:disappearance','build:disappoint:fancy',
            'build:disappoint:fancy:tend','build:disappoint:fancy:tend:conscience','build:disappoint:fancy:tend:conscience:relation',
            'build:disappoint:fancy:tend:conscience:winter','build:disappoint:fancy:tend:conscience:winter:and','build:disappoint:disappoint',
            'build:bottle','build:luck','build:nursery','build:disappearance','disappearance','proof','proof:fruit','proof:paste',
            'proof:paste:nest','proof:paste:cultivation','proof:paste:and','proof:respect'
        ]
        
        for i in range(15):
            l = random.randint(1, 5)
            t = random.choices(tags, k=l)
            res = connector.new_resource(f"Resource {i}", TAG_SPLITTER.join(t))
            manager.add_resource(res)
    else:
        connector = SQLiteResourceConnector(manager, db_path)
        connector.load_resources()

    atexit.register(connector.close)
    app.run(host="localhost", port="5428", debug=True)