from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy.orm.query import Query
from .models import db


def constructDBQuery(tablename: Model, filters: list) -> Query:
    '''Dynamically constructs a query from the filters given
    
    each filter should be::
    
        (parameter: str, value: any, operation: str)
    for the "like" and "or" operations each filter should be::
    
        ([parameter1_name: str, parameter2_name: str], [value1: any, value2: any], operation: str)
    
    posible operations::
        eq -> ==\n
        lt -> <\n
        gt -> >\n
        ge -> >=\n
        le -> <=\n
        nt -> !=\n
        like\n
        or
    '''
    
    # using getarrt() to grab the column and perform the operations on it
    query = db.session.query(tablename)
    for _filter, value, operation in filters:
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