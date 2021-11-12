import sqlite3 as sql
from datetime import datetime, time, timedelta
import pandas as pd

TIME_FORMAT = '%Y-%m-%d %H:%M'
TIME_FORMAT_SHORT = '%Y-%m-%d'
QUERY_SELECT = 'SELECT report_time, part_of_day, weight FROM weight'
QUERY_INSERT_DICT = '''
INSERT INTO weight (id, report_time, part_of_day, weight, who)
VALUES (:id, :report_time, :part_of_day, :weight, :who)
'''
QUERY_FIND = '''
SELECT * weight FROM  WHERE report_time
'''

def import_data():
    '''
    Import data from DB only with necessery columns acording to specify query. 
        Args: 
        Return: pd.DataFrame
    '''
    with sql.connect('data/data.db') as conn:
        df = pd.read_sql(QUERY_SELECT, conn, parse_dates=['report_time'])
        df['report_time'] = df['report_time'].dt.strftime(TIME_FORMAT_SHORT) 
        return df

def create_new_data_dict(weight: float, user: str ='Mateusz'):
    '''
    Create new data which in other functions will be updated to database. Functions check if new data exists in database.
    Args:
        - weight: user weight from UI,
        - user: specify which user put data into DB.
    Return:
        - dict
    '''
    current_time = datetime.now()
    current_time_str =  current_time.strftime(TIME_FORMAT)
    current_time_str_short = current_time.strftime(TIME_FORMAT_SHORT)

    if current_time.hour <= 12:
        part_of_day = 'morning'
    else:
        part_of_day = 'evening'

    data_id = f'{current_time_str_short}_{part_of_day}'
    db_ids = read_all_id()

    if data_id in db_ids:
        return None

    new_data = {
        'id': data_id,
        'report_time': current_time_str,
        'part_of_day': part_of_day,
        'weight': weight,
        'who': user
    }
    return new_data

def add_new_data(weight: float, user: str ='Mateusz'):
    '''
    Insert into DB new data. If data exists in DB insert empty dict.
    Args:
        - weight: user weight from UI,
        - user: specify which user put data into DB.
    Return:
        - dict
    '''
    new_data_dict = create_new_data_dict(weight, user)
    if new_data_dict is None:
        return {}   

    with sql.connect('data/data.db') as conn:
        conn.execute(QUERY_INSERT_DICT, new_data_dict)
        conn.commit()
        return new_data_dict

def remove_last_register(report_time: str):
    '''
    Remove last added register. App save in store last added row. User with this function can remove data.
    Args: 
        - report_time: 
    '''
    QUERY_FIND = f'SELECT *  FROM weight WHERE report_time = "{report_time}" '
    QUERY_REMOVE = f'DELETE FROM weight WHERE report_time = "{report_time}" '

    with sql.connect('data/data.db') as conn:
        result = conn.execute(QUERY_FIND).fetchall()
        if result:
            conn.execute(QUERY_REMOVE)
            conn.commit()
    return None

def read_all_id():
    '''
    Read from DB all id to check if new data exists.   
    Args:
    Return:
        - set
    '''
    q = 'SELECT id FROM weight'
    with sql.connect('data/data.db') as conn:
        result = conn.execute(q).fetchall()
        return {id[0] for id in result}

def read_last_date():
    q = 'SELECT MAX(report_time) FROM weight'
    with sql.connect('data/data.db') as conn:
        result = conn.execute(q).fetchone()[0]
        return datetime.strptime(result, TIME_FORMAT) 

if __name__ == '__main__':
    # print(import_data())
    print(create_new_data_dict(82.0))
    # print(add_new_data(82.6))
    # print(import_data())
    # print(read_all_id())