from flask import Flask
import sqlite3
import os
from os import path
from uuid import uuid4

app = Flask(__name__)

TAG_HIER = ":"
TAG_SPLITTER = ";;"



# class Tag: # #Type:SubType:..:Tag
#     pass
class TagStr(str): # only str of node, no ":"
    pass
class TagStrFull(str): # full tag str, L1:L2:...:Ln
    pass

class Resource:
    """The minimum representor of a resource"""
    def __init__(self, name: str, tags_str: str=None, bound_object=None):
        self.name = name
        self.tags: list[TagStrFull] = [] if tags_str is None or tags_str=='' else tags_str.split(TAG_SPLITTER) # use list[str] or list[object]?
        self.bound_object = bound_object

    @property
    def tags_str(self):
        return TAG_SPLITTER.join(self.tags)

    def update_tags(self, from_tags: list[TagStrFull], to_tags: list[TagStrFull]):
        pass

        # when to sync to save the changes?

    def update_content(self):
        ... # needed?

    def flush_update(self):
        ...

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Resource<{self.name}>"
    
class TagNode:
    """TagNode hold related resources attached to the tag, and form a tree with parent/child relationship"""
    def __init__(self, tag_str: TagStr, parent_node: "TagNode"=None):
        self.tag_str = tag_str # assert ":" not in tag_str
        self.resources: set[Resource] = set()

        self.parent_node: TagNode = parent_node
        self.sub_nodes: dict[TagStr, TagNode] = {}

    def add_subnode(self, tag_node: "TagNode"):
        self.sub_nodes[tag_node.tag_str] = tag_node # what if already exist, and the resources are not merged

    def collect_resources(self, collection: list[Resource]=None):
        if collection is None:
            collection = []

        collection.extend(self.resources)

        for sub_tree in self.sub_nodes.values():
            sub_tree.collect_resources(collection)

        return collection
    
    # @cache
    def _recalc_full_tag_str(self):
        if self.parent_node is None:
            return self.tag_str
        else:
            return self.parent_node._recalc_full_tag_str()+TAG_HIER+self.tag_str
        
    def __repr__(self):
        return str(self)
        
    def __str__(self):
        return f"Tag<{self._recalc_full_tag_str()}>"

class Manager:
    """The storage of all tags and resources"""
    def __init__(self) -> None:
        self._root_node = TagNode(tag_str='')
        self._tag_map: dict[TagStrFull, TagNode] = {'': self._root_node}
        # self._lock # when renaming tag
    
    def get_or_create_tag(self, full_tag_str: TagStrFull) -> "TagNode":
        tag_node = self._tag_map.get(full_tag_str)
        if tag_node is None:
            if TAG_HIER in full_tag_str:
                parent_tag_str, tag_str = full_tag_str.rsplit(TAG_HIER, 1)
                # if tag_str==""
                parent_node = self.get_or_create_tag(parent_tag_str)
                tag_node = TagNode(tag_str, parent_node=parent_node)
                parent_node.add_subnode(tag_node)
            else:
                tag_node = TagNode(full_tag_str)
                self._root_node.add_subnode(tag_node) # so root has subnodes, but 1st layer nodes has not parent
            self._tag_map[full_tag_str] = tag_node
        return tag_node

    # @cache
    def get_tags_of(self, full_tag_str:TagStrFull="") -> list[str]:
        # only return 1 layer
        return [tag_node_str for tag_node_str in self._tag_map[full_tag_str].sub_nodes]

    def add_resource(self, resource: Resource):
        for full_tag_str in resource.tags:
            tag_node = self.get_or_create_tag(full_tag_str)
            tag_node.resources.add(resource)

    # @cache
    def get_resources(self, ) -> list[Resource]:
        # to save the info (e.g., save as json if tags are not stored in resource itself)
        pass

    def filter_resources(self, tags: list[TagStrFull]) -> list[Resource]:
        # TODO: extends to multiple operands
        final_res = None
        for full_tag_str in tags:
            tag_node = self._tag_map.get(full_tag_str)
            if tag_node is None:
                sub_res = set()

                final_res = None
                break # since the intersection will always be empty
            else:
                sub_res = set(tag_node.collect_resources())

            if final_res is None:
                final_res = sub_res
            else:
                final_res.intersection_update(sub_res)

        if final_res is None:
            return []
        else:
            return list(final_res)

    def rename_tag(self, from_tag: TagStrFull, to_tag: TagStrFull): # also for tag-duplication case, e.g. hello == hi, created by different users
        # need to lock

        # 1. change the tagstr for resources
        # 2. change the _tag_map keys
        # 3. move node and its subnodes
        pass

    def tree_print(self, node: TagNode=None, depth: int=0):
        if node is None:
            node = self._root_node

        print('-'*depth, node, node.resources or '')

        for sub_node in node.sub_nodes.values():
            self.tree_print(sub_node, depth=depth+1)



class ResourceConnector:
    def __init__(self, manager: Manager):
        self.manager = manager

    def load_resources(self):
        ...

    def save_resources(self):
        ...

    def new_resource(self, name: str, tags_str: str) -> Resource:
        ...

class SQLiteResource(Resource):
    def __init__(self, id: int, name: str, tags_str: str, conn: sqlite3.Connection):
        super().__init__(name=name, tags_str=tags_str)

        self.id = id
        self.conn = conn

    def __str__(self):
        return f"SQLiteResource<{self.name} @ {self.id}>"
    
    def flush_update(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE resources
            SET ResourceName = ?, Tags = ?
            WHERE ID = ?
        ''', (self.name, self.tags_str, self.id))
        self.conn.commit()

class SQLiteResourceConnector(ResourceConnector):
    def __init__(self, manager: Manager, db_path: str):
        super().__init__(manager)

        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ResourceName TEXT NOT NULL,
                Tags TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def load_resources(self):
        self.cursor.execute('SELECT ID, ResourceName, Tags FROM resources')
        rows = self.cursor.fetchall()
        
        for row in rows:
            id, resource_name, tags_str = row
            resource = SQLiteResource(id, resource_name, tags_str, self.conn)
            self.manager.add_resource(resource)

    def new_resource(self, name: str, tags_str: str) -> SQLiteResource:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO resources (ResourceName, Tags)
            VALUES (?, ?)
        ''', (name, tags_str))
        self.conn.commit()
        resource_id = cursor.lastrowid

        return SQLiteResource(resource_id, name, tags_str, self.conn)
    
    def close(self):
        self.conn.close()

class FileResource(Resource):
    def __init__(self, uuid: str, name: str, tags_str: str, storage_dir: str):
        super().__init__(name=name, tags_str=tags_str)

        self.uuid = uuid
        self.storage_dir = storage_dir

    def __str__(self):
        return f"FileResource<{self.name} @ {self.uuid}>"

    def flush_update(self):
        with open(path.join(self.storage_dir, self.uuid), mode='w') as fp: # caution 'w' truncate, change it if more content inside the file
            fp.write(self.name+"\n")
            fp.write(self.tags_str+"\n")

class FileResourceConnector(ResourceConnector):
    def __init__(self, manager: Manager, storage_dir: str):
        super().__init__(manager)
        self.storage_dir = storage_dir

    def load_resources(self):
        for f in os.listdir(self.storage_dir):
            with open(path.join(self.storage_dir, f), mode='r') as fp:
                name = fp.readline().strip()
                tags_str = fp.readline().strip()
                resource = FileResource(f, name, tags_str, self.storage_dir)
                self.manager.add_resource(resource)
    
    def new_resource(self, name: str, tags_str: str) -> FileResource:
        uuid = uuid4().hex
        resource = FileResource(uuid, name, tags_str, self.storage_dir)
        resource.flush_update()
        return resource



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
    res1.tags.append("Project:Project1")
    res1.tags.append("Analysis:Analysis1")
    manager.add_resource(res1)

    connector = SQLiteResourceConnector(manager, db_path='../storage/resources.db')
    connector.load_resources()
    res2 = connector.new_resource("Project2 analysis2 resource", "Project:Project2;;Analysis:Analysis2")
    manager.add_resource(res2)

    app.run(host="localhost", port="5428", debug=True)

    # database for result_stat/various_resource/data_info/...