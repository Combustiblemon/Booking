from flask_restful import abort
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session


def constructDBQuery(tablename, criteria: list, session: Session) -> Query:
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
    '''
    query = session.query(tablename)
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
    
    return query.limit(150)