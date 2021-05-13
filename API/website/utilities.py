from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy.orm.query import Query
from .models import db


def constructDBQuery(tablename: Model, criteria: list) -> Query:
    '''
    Criteria should be::
        ('parameter', value, 'operation')
    
    posible operations::
        eq -> ==\n
        lt -> <\n
        gt -> >\n
        ge -> >=\n
        le -> <=\n
        nt -> !=
        like
        or
    '''
    query = db.session.query(tablename)
    for _filter, value, operation in criteria:
        operation.lower().strip()
        if operation == 'eq':
            query = query.filter(getattr(tablename, _filter) == value)
        elif operation == 'lt':
            query = query.filter(getattr(tablename, _filter) < value)
        elif operation == 'gt':
            query = query.filter(getattr(tablename, _filter) > value)
        elif operation == 'ge':
            query = query.filter(getattr(tablename, _filter) >= value)
        elif operation == 'le':
            query = query.filter(getattr(tablename, _filter) <= value)
        elif operation == 'nt':
            query = query.filter(getattr(tablename, _filter) != value)
        elif operation == 'like':
            query = query.filter(getattr(tablename, _filter).like(f"%{value}%"))
        elif operation == 'or':
            query = query.filter(getattr(tablename, _filter[0]).like(f"%{value[0]}%") | getattr(tablename, _filter[1]).like(f"%{value[1]}%"))
    
    return query.limit(150)

def getReturnObject(status_code: int = 0, **data) -> tuple:
    return (data, status_code)