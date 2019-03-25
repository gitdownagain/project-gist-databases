from .models import Gist

### NEED TO GO BACK AND REDO
DATETIME_PREFIXES = ('created_at', 'updated_at')

def is_datetime_param(param):
    for prefix in DATETIME_PREFIXES:
        if param.startswith(prefix):
            return True
    return False

# clever way to do substitution
def get_operator(comparison):
    return {
        'lt': '<',
        'lte': '<=',
        'gt': '>',
        'gte': '>=',
    }[comparison]
### NEED TO GO BACK AND REDO

def build_query(**kwargs):
    query = 'SELECT * FROM gists'
    values = {}
    
    if kwargs:
        filters = []
        for param, value in kwargs.items():
            if is_datetime_param(param):
                attribute = param
                filters.append('datetime(%s) == datetime(:%s)' % (attribute, param))
                values[param] = value
            else:
                filters.append('%s = :%s' % (param, param))
                values[param] = value

        query += ' WHERE '
        query += ' AND '.join(filters)

    return query, values

def search_gists(db_connection, **kwargs):
    query, params = build_query(**kwargs)
    cursor = db_connection.execute(query, params)
    
    # similar to Get Movies and Directors
    # https://learn.rmotr.com/python/base-python-track/database-handling/get-movies-and-directors
    
    results = []
    
    for gist in cursor:
        results.append(Gist(gist))
    
    return results
