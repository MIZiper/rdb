from flask import Flask, jsonify, request
from rtm import TagStr, TagStrFull, Manager, Resource
from flask_cors import CORS

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
    resources = manager.get_resources()
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
    from rtm import SQLiteResourceConnector
    
    res1 = Resource("Project1 analysis1 resource")
    res1.tags.append("Project:Project1")
    res1.tags.append("Analysis:Analysis1")
    manager.add_resource(res1)

    connector = SQLiteResourceConnector(manager, db_path='../storage/resources.db')
    connector.load_resources()
    res2 = connector.new_resource("Project2 analysis2 resource", "Project:Project2;;Analysis:Analysis2")
    manager.add_resource(res2)

    app.run(host="localhost", port="5428", debug=True)

    # database for result_stat/various_resource/data_info/...