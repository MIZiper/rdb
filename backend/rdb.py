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
    def __init__(self, id: int, name: str, tags_str: TagsFullStr, conn: sqlite3.Connection):
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

    def new_resource(self, name: str, tags_str: TagsFullStr) -> SQLiteResource:
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

if __name__=="__main__":
    # Example setup for SQLAlchemy
    engine = create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()