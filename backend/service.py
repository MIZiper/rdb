from flask import Flask

app = Flask(__name__)



# class Tag: # #Type:SubType:..:Tag
#     pass
class TagStr(str): # only str of node, no ":"
    pass
class TagStrFull(str): # full tag str, L1:L2:...:Ln
    pass

class Resource:
    """The minimum representor of a resource"""
    def __init__(self, bound_object=None):
        self.bound_object = bound_object
        self.tags: list[TagStrFull] = []

    def update_tags(self, from_tags: list[TagStrFull], to_tags: list[TagStrFull]):
        pass
    
class TagNode:
    """TagNode hold related resources attached to the tag, and form a tree with parent/child relationship"""
    def __init__(self, tag_str: TagStr):
        self.tag_str = tag_str # assert ":" not in tag_str
        self.resources: set[Resource] = set()

        self.parent_node: TagNode = None
        self.sub_nodes: dict[TagStr, TagNode] = {}

    def collect_resources(self, collection: list[Resource]=None):
        if collection is None:
            collection = []

        collection.extend(self.resources)

        for sub_tree in self.sub_nodes.values():
            sub_tree.collect_resources(collection)

        return collection
    
    def _recalc_full_tag_str(self):
        pass

    @staticmethod
    def create_tagnode_for(manager: "Manager", tag_str_full: TagStrFull) -> "TagNode":
        ...

class Manager:
    """The storage of all tags and resources"""
    def __init__(self) -> None:
        self._tag_map: dict[TagStrFull, TagNode] = {}

    # @cache
    def get_tags_of(self, full_tag_str:TagStrFull="") -> list[str]:
        # only return 1 layer
        return [tag_node_str for tag_node_str in self._tag_map[full_tag_str].sub_nodes]

    def filter_resources(self, tags: list[TagStrFull]) -> list[Resource]:
        # use set {}
        pass

    def add_resource(self, resource: Resource):
        for full_tag_str in resource.tags:
            tag_node = self._tag_map.get(full_tag_str)
            if tag_node is None:
                ... # create recursively
            else:
                # assert resource not in tag_node.resources
                tag_node.resources.add(resource)

    def get_resources(self) -> list[Resource]:
        # to save the info (e.g., save as json if tags are not stored in resource itself)
        pass

    def rename_tag(self, from_tag: TagStrFull, to_tag: TagStrFull): # also for tag-duplication case, e.g. hello == hi, created by different users
        pass



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

@app.route("/resources/<string:resource>", methods=['POST'])
def add_resource_with_tags(resource: str):
    pass

if __name__=="__main__":
    manager = Manager()

    res1 = Resource("Project1 analysis1 resource")
    manager.add_resource(res1, [
        "Project:Project1",
        "Analysis:Analysis1"
    ])

    app.run(host="localhost", port="5428", debug=True)

    # database for result_stat/various_resource/data_info/...