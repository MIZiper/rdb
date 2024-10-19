"""RDB implementation based on RTM
"""

from datetime import datetime

class ResultFile:
    Link2Analysis = ''
    ModuleName = 'Unspecified'
    Tags: list[str] = []

    Title: str
    AddDate: datetime
    UpdateDate: datetime

class ResultData:
    # auto implement the table/markdown/XY
    # enable fast inheritance of DataType creation, able to customize for e.g. photos
    def to_file(self):
        ...

    def from_file(self):
        ...