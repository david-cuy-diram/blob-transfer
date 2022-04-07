import Environment as env
import json
import decimal
import datetime
from typing import List
import sqlalchemy
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.session import Session as ORMSession, sessionmaker

## Database connection string
connect_url = f'''mssql+pyodbc://{env.DB_USER}:{env.DB_PWD}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}?driver={env.DB_DRIVER}'''
__engine = sqlalchemy.create_engine(connect_url, echo=False)
__Session = sessionmaker(bind=__engine)


def get_session() -> ORMSession:
    """ Return a new database session from engine to data access

    Returns:
        ORMSession: Database session
    """
    return __Session()

def get_engine() -> Engine:
    """ Return the database engine

    Returns:
        Engine: Database Engines
    """
    return __engine


class AlchemyEncoder(json.JSONEncoder):
    """ Based on: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json/41204271 """
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            property_map = obj.property_map()
            for field in [x for x in obj.attrs]:
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, (datetime.datetime, datetime.date)):
                        data = data.isoformat()
                    else:
                        json.dumps(data)
                    fields[property_map[field] if field in property_map else field] = data
                except TypeError:
                    fields[field] = None
            return fields
        if isinstance(obj, decimal.Decimal):
            if obj % 1 > 0:
                return float(obj)
            else:
                return int(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

class AlchemyRelationEncoder(json.JSONEncoder):
    def __init__(self, relationships: List[str], **kwargs) -> None:
        super().__init__(**kwargs)
        self.relationships = relationships
        
    """ Based on: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json/41204271 """
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            property_map = obj.property_map()
            
            relation_names = [attr for attr, relation in obj.__mapper__.relationships.items()]
            filters_model = list(set(self.relationships).intersection(relation_names))
            attributes = [x for x in obj.attrs]
            
            if type(filters_model) is list:
                attributes.extend(filters_model)
            
            for field in attributes:
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, (datetime.datetime, datetime.date)):
                        data = data.isoformat()
                    else:
                        json.dumps(data, cls=self.__class__, check_circular=self.check_circular, relationships=self.relationships)
                    fields[property_map[field] if field in property_map else field] = data
                except TypeError as e:
                    fields[field] = None
            return fields
        if isinstance(obj, decimal.Decimal):
            if obj % 1 > 0:
                return float(obj)
            else:
                return int(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

