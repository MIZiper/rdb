"""Resource Tag Manager
"""

import sqlite3
import os
from os import path
from uuid import uuid4

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

    def merge_from(self, ano_node: "TagNode"):
        # NOTE: the resources.tags from `ano_node` and its sub_nodes should be correctly mantained elsewhere

        if self is ano_node:
            return
        # assert ano_node.tag_str == self.tag_str
        self.resources.update(ano_node.resources)
        for sub_node in ano_node.sub_nodes.values():
            self.add_subnode(sub_node)

    def add_subnode(self, tag_node: "TagNode"):
        if (orig_node := self.sub_nodes.get(tag_node.tag_str)) is None: # simply add it, no conflict
            self.sub_nodes[tag_node.tag_str] = tag_node
            tag_node.parent_node = self
        else:
            orig_node.merge_from(tag_node)

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
        self._root_node = TagNode(tag_str='[VirtualRoot]')
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
                self._root_node.add_subnode(tag_node)
                tag_node.parent_node = None # so root has subnodes, but 1st layer nodes has not parent
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
        
    def update_resource_tags(self, resource: Resource, tags: list[TagStrFull]):
        from_set = set(resource.tags)
        to_set = set(tags)

        remove_from = from_set - to_set
        add_to = to_set - from_set

        if not remove_from and not add_to: # same
            return

        for from_tag in remove_from:
            tag_node = self._tag_map.get(from_tag)
            if tag_node is None:
                continue
            tag_node.resources.remove(resource)

        for to_tag in add_to:
            tag_node = self.get_or_create_tag(to_tag)
            tag_node.resources.add(resource)

        resource.tags = tags.copy()
        resource.flush_update()

    def rename_tag(self, from_tag: TagStrFull, to_tag: TagStrFull): # also for tag-duplication case, e.g. hello == hi, created by different users
        # need to lock

        tag_map = self._tag_map

        from_node = tag_map.get(from_tag)
        if from_node is None or from_tag==to_tag or not from_tag or not to_tag:
            return
        
        # 1. change the tagstr for resources
        resources_2b_updated: set[Resource] = set(from_node.collect_resources())
        for resource in resources_2b_updated:
            resource.tags = [
                tag_str.replace(from_tag, to_tag, 1) if tag_str.startswith(from_tag) else tag_str
                for tag_str in resource.tags
            ]
            # resource.flush_update()?

        # 3. move node and its subnodes
        parent_node = from_node.parent_node or self._root_node
        node = parent_node.sub_nodes.pop(from_node.tag_str) # remove from parent
        assert node is from_node
        to_node = self.get_or_create_tag(to_tag)
        to_node.merge_from(from_node)

        # 2. change the tag_map keys
        for key in list(tag_map.keys()):
            if not key.startswith(from_tag):
                continue
            
            node = tag_map.pop(key)
            new_key = key.replace(from_tag, to_tag, 1)
            if new_key in tag_map:
                # assert node._recalc_full_tag_str() == key
                pass # tag_map[new_key] `merge_from` node in step 3
            else:
                # assert node._recalc_full_tag_str() == new_key # already rebound
                tag_map[new_key] = node
            # is there a way to combine step 2 & 3, both steps need to handle already-existed case

            # one optimization can be:
            # - run step 3 first, and get a list of path-es need updated/merged
            # - no need to iterate full keys, just update the affected ones

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