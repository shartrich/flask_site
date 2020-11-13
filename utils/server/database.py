from pymysql import connect, cursors
import pandas as pd
from sqlalchemy import create_engine
from utils.configs.settings import DB_USERNAME, DB_PASSWORD, DB_DATABASE, DB_HOST
import sys


def create_connection(database=DB_DATABASE):
    """connect to the DB with the user's credentials"""
    connection = connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        db=database,
        # port=tunnel.local_bind_port,
        cursorclass=cursors.DictCursor
    )
    return connection

def sql_engine(database=DB_DATABASE):
    engine_string = "mysql+pymysql://{user}:{password}@{host}/{db}".format(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            db=database,
        )
    return create_engine(
        engine_string,
        encoding='latin1', 
        # echo=True
        )

def get_query_from_body(request):
    body = request.json()
    print(body)
    return body.get('query', 'SHOW DATABSES;')


def handle_database_request(request):
    query = request.args.get('query', default=None, type=str)
    if not query:
        query = get_query_from_body(request)
    
    print('query:', query)
    response = {'success': True}
    try:
        if 'select' in query:
            conn = sql_engine()
            df = pd.read_sql_query(query, conn)
            response['results'] = df.to_dict('records')
        else:
            conn = create_connection()
            cursorObject = conn.cursor()
            cursorObject.execute(query)
            conn.close()
            response['results'] = cursorObject.fetchall()
    except:
        print('DATABASE ERROR:')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print(sys.exc_info()[2])
        response['error'] = str(sys.exc_info())
        response['success'] = False
    return response


