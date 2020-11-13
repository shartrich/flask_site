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

def handle_database_request(request):
    query = request.args.get('query', default='SHOW DATABSES;', type=str)
    print(request.method)
    if request.method == 'POST':
        body = request.json()
        print(body)
        query = body.get(query, 'SHOW DATABSES;')
    
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
        response['error'] = sys.exc_info()[0]
        response['success'] = False
    return response


