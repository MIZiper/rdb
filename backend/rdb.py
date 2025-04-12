"""RDB implementation based on RTM
"""

from datetime import datetime
from rtm import Resource, TagsFullStr, Manager, TAG_SPLITTER

from sqlalchemy import Column, String, DateTime, BINARY, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from modules import RecordContentHandler



Base = declarative_base()

class ResourceRecord(Base):
    __tablename__ = 'resources'

    UUID = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    ModuleInfo = Column(String, default='ModuleName;;v0.0.1')
    Tags = Column(String, default='')
    AddDate = Column(DateTime, default=datetime.now)
    UpdateDate = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    Link = Column(String, default='')
    Description = Column(String, default='')
    Content = Column(String, default='')

    def to_detail_dict(self):
        return {
            'uuid': self.UUID,
            'title': self.Title,
            'tags': self.Tags,
            'update_date': self.UpdateDate,
            'description': self.Description,
            'module': self.ModuleInfo,
            'link': self.Link,
            'content': self.Content,
        }
    
    def to_meta_dict(self):
        return {
            'uuid': self.UUID,
            'title': self.Title,
            'tags': self.Tags,
            'update_date': self.UpdateDate,
            'description': self.Description,
        }
    
R = ResourceRecord
LEAN_FIELDS = (R.UUID, R.Title, R.Tags) # for rtm
META_FIELDS = (R.UUID, R.Title, R.Tags, R.UpdateDate, R.Description) # for resource list



class SQLiteResource(Resource):
    def __init__(self, id: int, title: str, tags_str: TagsFullStr, session):
        super().__init__(res_id=id, tags_str=tags_str)
        self.title = title
        self.session = session

    def flush_tags_update(self):
        # or cache the records to be updated, and update in bunch
        record = self.session.query(*LEAN_FIELDS).filter_by(UUID=self.res_id).first()
        record.Tags = self.tags_str
        self.session.commit()

    def __str__(self):
        return f"SQLiteResource<{self.title}@{self.res_id}>"

class SQLiteController:
    def __init__(self, manager: Manager, db_path: str):
        self.manager = manager
        self.db_path = db_path

        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    @property
    def total_resources(self):
        return self.session.query(ResourceRecord).count()

    def load_resources(self):
        records = self.session.query(*LEAN_FIELDS).all()
        for record in records:
            sqlite_resource = SQLiteResource(record.UUID, record.Title, record.Tags, self.session)
            self.manager.add_resource(sqlite_resource)

    def new_resource(self, title: str, tags_str: TagsFullStr,
                     description: str="", link: str="", content: str="", module_info: str="",
                     ) -> ResourceRecord:
        new_record = ResourceRecord(
            Title=title,
            Tags=tags_str,
            Description=description,
            Link=link,
            Content=content,
            ModuleInfo=module_info
        )
        self.session.add(new_record)
        self.session.commit()

        new_resource = SQLiteResource(new_record.UUID, title, tags_str, self.session)
        self.manager.add_resource(new_resource)

        return new_record
    
    def get_meta_records_by_page(self, page: int, items_per_page: int=7) -> list[ResourceRecord]:
        return self.session.query(*META_FIELDS).order_by(ResourceRecord.UUID.desc()).limit(items_per_page).offset(page*items_per_page).all()
    
    def get_meta_records_by_ids(self, ids: list[int]) -> list[ResourceRecord]:
        return self.session.query(*META_FIELDS).filter(ResourceRecord.UUID.in_(ids)).all()
    
    def get_full_record_by_id(self, id: int) -> ResourceRecord:
        return self.session.query(ResourceRecord).filter_by(UUID=id).first()
    
    def close(self):
        self.session.close()



if __name__=="__main__":
    engine = create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()