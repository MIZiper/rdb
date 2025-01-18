from flask import Flask, jsonify, request
from rtm import TagStr, TagStrFull, Manager, Resource, TAG_SPLITTER
from flask_cors import CORS
import atexit

app = Flask(__name__)
CORS(app)
manager = Manager()



@app.route("/tags", defaults={'tag': ''}, methods=['GET']) # equal to `/tags/<empty>`
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
    resources = manager.get_all_resources()
    return jsonify([resource.to_dict() for resource in resources])

@app.route("/resources/<string:resource>", methods=['GET'])
def show_resource(resource: str):
    resource_obj = manager.get_resource(resource)
    if not resource_obj:
        return jsonify({'error': 'Resource not found'}), 404
    return jsonify(resource_obj.to_dict())

@app.route("/resources", methods=['POST'])
def add_resource_with_tags():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Resource name is required'}), 400
    
    tags = data.get('tags', '')  # Optional tags string (tag1;;tag2;;tag3)
    resource = Resource(data['name'])
    if tags:
        for tag in tags.split(';;'):
            resource.tags.append(tag)
    
    manager.add_resource(resource)
    return jsonify({'message': 'Resource created successfully'}), 201



if __name__=="__main__":
    from rdb import SQLiteResourceConnector
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