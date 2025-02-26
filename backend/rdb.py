"""RDB implementation based on RTM
"""

import sqlite3
from uuid import uuid4
from datetime import datetime
from rtm import Resource, TagsFullStr, Manager, ResourceConnector

from sqlalchemy import Column, String, DateTime, BINARY, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



Base = declarative_base()

class ResultRecord(Base):
    __tablename__ = 'result_records'

    UUID = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    ModuleInfo = Column(String, default='ModuleName;;v0.0.1')
    Tags = Column(String, default='')
    AddDate = Column(DateTime, default=datetime.utcnow)
    UpdateDate = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    Link = Column(String, default='')
    Description = Column(String, default='')
    Content = Column(String, default='')

    def to_blob(self) -> bytes:
        # Implement the logic to convert the object to a blob
        pass

    def from_blob(self) -> bytes:
        # Implement the logic to convert the blob back to the object
        pass



class SQLiteResource(Resource):
    def __init__(self, id: int, name: str, tags_str: TagsFullStr, session):
        super().__init__(res_id=id, tags_str=tags_str)
        self.id = id
        self.name = name
        self.session = session

    def __str__(self):
        return f"SQLiteResource<{self.name} @ {self.id}>"
    
    def flush_tags_update(self):
        resource = self.session.query(ResultRecord).filter_by(UUID=self.id).first()
        resource.Tags = self.tags_str
        self.session.commit()

    def to_dict(self):
        return {
            'uuid': self.id,
            'name': self.name,
            'tags': self.tags,
        }
    
    def to_meta_dict(self):
        resource = self.session.query(ResultRecord).filter_by(UUID=self.id).first()
        return {
            'uuid': resource.UUID,
            'name': resource.Title,
            'tags': self.tags,
            'update_date': resource.UpdateDate,
            'description': resource.Description
        }

    def to_detail_dict(self):
        resource = self.session.query(ResultRecord).filter_by(UUID=self.id).first()
        return {
            'uuid': resource.UUID,
            'name': resource.Title,
            'tags': self.tags,
            'update_date': resource.UpdateDate,
            'description': resource.Description,
            'type': resource.ModuleInfo,
            'link': resource.Link,
            'content': resource.Content
        }

class SQLiteResourceConnector(ResourceConnector):
    def __init__(self, manager: Manager, db_path: str):
        super().__init__(manager)
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    @property
    def total_resources(self):
        return self.session.query(ResultRecord).count()

    def load_resources(self):
        resources = self.session.query(ResultRecord).all()
        for resource in resources:
            sqlite_resource = SQLiteResource(resource.UUID, resource.Title, resource.Tags, self.session)
            self.manager.add_resource(sqlite_resource)

    def new_resource(self, name: str, tags_str: TagsFullStr,
                     description: str="", link: str="", content: str="", module_info: str="",
                     ) -> SQLiteResource:
        new_record = ResultRecord(
            Title=name,
            Tags=tags_str,
            Description=description,
            Link=link,
            Content=content,
            ModuleInfo=module_info
        )
        self.session.add(new_record)
        self.session.commit()
        return SQLiteResource(new_record.UUID, name, tags_str, self.session)
    
    def get_resources_by_page(self, page: int, items_per_page: int=7) -> list[SQLiteResource]:
        resources = self.session.query(ResultRecord).order_by(ResultRecord.UUID.desc()).limit(items_per_page).offset(page*items_per_page).all()
        return [SQLiteResource(resource.UUID, resource.Title, resource.Tags, self.session) for resource in resources]
    
    def get_resources_by_ids(self, ids: list[str]) -> list[SQLiteResource]:
        resources = self.session.query(ResultRecord).filter(ResultRecord.UUID.in_(ids)).all()
        return [SQLiteResource(resource.UUID, resource.Title, resource.Tags, self.session) for resource in resources]
    
    def get_resource(self, id: int) -> SQLiteResource:
        resource = self.session.query(ResultRecord).filter_by(UUID=id).first()
        return SQLiteResource(resource.UUID, resource.Title, resource.Tags, self.session)
    
    def close(self):
        self.session.close()

if __name__=="__main__":
    # Example setup for SQLAlchemy
    engine = create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()