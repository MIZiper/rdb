"""RDB implementation based on RTM
"""

import sqlite3
from uuid import uuid4
from datetime import datetime
from rtm import Resource, TagsFullStr, Manager, ResourceConnector

from sqlalchemy import Column, String, DateTime, BINARY, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



Base = declarative_base()

class ResultRecord(Base):
    __tablename__ = 'result_records'

    UUID = Column(String, primary_key=True, default=lambda: str(uuid4()))
    Title = Column(String, nullable=False)
    Link2Analysis = Column(String, default='')
    ModuleInfo = Column(String, default='ModuleName;;v0.0.1')
    Tags = Column(String, default='')
    AddDate = Column(DateTime, default=datetime.utcnow)
    UpdateDate = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    BoundObject = Column(BINARY, nullable=True)

    def to_blob(self) -> bytes:
        # Implement the logic to convert the object to a blob
        pass

    def from_blob(self) -> bytes:
        # Implement the logic to convert the blob back to the object
        pass



class SQLiteResource(Resource):
    # NOTE: the object doesn't need to be inside a `manager`
    def __init__(self, id: int, name: str, tags_str: TagsFullStr, conn: sqlite3.Connection):
        super().__init__(res_id=id, tags_str=tags_str)

        self.id = id
        self.name = name
        self.conn = conn

    def __str__(self):
        return f"SQLiteResource<{self.name} @ {self.id}>"
    
    def flush_tags_update(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE resources
            SET Tags = ?
            WHERE ID = ?
        ''', (self.tags_str, self.id))
        self.conn.commit()

    def to_dict(self):
        return {
            'name': self.name,
            'tags': self.tags
        }

class SQLiteResourceConnector(ResourceConnector):
    def __init__(self, manager: Manager, db_path: str):
        super().__init__(manager)

        self._total_resources = 0
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False) # temporary in multi-threads

        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ResourceName TEXT NOT NULL,
                Tags TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    @property
    def total_resources(self):
        if self._total_resources == 0:
            cursor = self.conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM resources')
            # if `deleted` column is added, then use `WHERE deleted=0`
            self._total_resources = cursor.fetchone()[0]
        return self._total_resources

    def load_resources(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT ID, ResourceName, Tags FROM resources')
        rows = cursor.fetchall()
        
        for row in rows:
            id, resource_name, tags_str = row
            resource = SQLiteResource(id, resource_name, tags_str, self.conn)
            self.manager.add_resource(resource)

    def new_resource(self, name: str, tags_str: TagsFullStr) -> SQLiteResource:
        # NOTE: the caller has to do `manager.add_resource`, but why not embed inside this function?
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO resources (ResourceName, Tags)
            VALUES (?, ?)
        ''', (name, tags_str))
        self.conn.commit()
        resource_id = cursor.lastrowid
        self._total_resources = 0 # reset the counter cache, same for delete

        return SQLiteResource(resource_id, name, tags_str, self.conn)
    
    def get_resources(self, page: int, items_per_page: int=7) -> list[SQLiteResource]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT ID, ResourceName, Tags
            FROM resources
            ORDER BY ID DESC
            LIMIT ? OFFSET ?
        ''', (items_per_page, page*items_per_page))

        rows = cursor.fetchall()
        resources = [SQLiteResource(id, resource_name, tags_str, self.conn) for id, resource_name, tags_str in rows]
        
        return resources
    
    def get_resource(self, id: int) -> SQLiteResource:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT ResourceName, Tags
            FROM resources
            WHERE ID = ?
        ''', (id,))

        resource_name, tags_str = cursor.fetchone()

        return SQLiteResource(id, resource_name, tags_str, self.conn)
    
    def close(self):
        self.conn.close()

if __name__=="__main__":
    # Example setup for SQLAlchemy
    engine = create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()