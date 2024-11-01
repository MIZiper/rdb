from flask import Flask
from rtm import TagStr, TagStrFull, Manager, Resource

app = Flask(__name__)
manager = Manager()



@app.route("/tags", defaults={'tag': ''}, methods=['GET']) # equal to `/tags/<empty>`
@app.route("/tags/<string:tag>", methods=['GET']) # list-sub
def list_tags_of(tag: TagStrFull):
    pass

@app.route("/tags", methods=['POST']) # create
def create_tag():
    pass

@app.route("/resources", methods=['GET'])
def show_resource_list(): # order by added date
    pass

@app.route("/resources/<string:resource>", methods=['GET'])
def show_resource(resource: str):
    pass

@app.route("/resources", methods=['POST'])
def add_resource_with_tags():
    pass



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