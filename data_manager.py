import sqlite3 as sql
from datetime import datetime, time, timedelta
import pandas as pd

TIME_FORMAT = '%Y-%m-%d %H:%M'
TIME_FORMAT_SHORT = '%Y-%m-%d'
QUERY_SELECT = 'SELECT report_time, part_of_day, weight, who FROM weight'
QUERY_INSERT_DICT = '''
INSERT INTO weight (report_time, part_of_day, weight, who)
VALUES (:report_time, :part_of_day, :weight, :who)
'''
QUERY_FIND = '''
SELECT * weight FROM  WHERE report_time
'''

def import_data():
    with sql.connect('data/data.db') as conn:
        df = pd.read_sql(QUERY_SELECT, conn, parse_dates=['report_time'])
        df['report_time'] = df['report_time'].dt.strftime(TIME_FORMAT_SHORT) 
        return df

def create_new_data_dict(weight: float, user: str ='Mateusz'):
    current_time = datetime.now()
    current_time_str =  current_time.strftime(TIME_FORMAT)

    if current_time.hour <= 12:
        part_of_day = 'morning'
    else:
        part_of_day = 'evening'

    new_data = {
        'report_time': current_time_str,
        'part_of_day': part_of_day,
        'weight': weight,
        'who': user
    }
    return new_data

def add_new_data(weight: float, user: str ='Mateusz'):
    new_data_dict = create_new_data_dict(weight, user)
    with sql.connect('data/data.db') as conn:
        conn.execute(QUERY_INSERT_DICT, new_data_dict)
        conn.commit()
    return new_data_dict

def remove_last_register(report_time: str):
    QUERY_FIND = f'SELECT *  FROM weight WHERE report_time = "{report_time}" '
    QUERY_REMOVE = f'DELETE FROM weight WHERE report_time = "{report_time}" '

    with sql.connect('data/data.db') as conn:
        result = conn.execute(QUERY_FIND).fetchall()
        if result:
            conn.execute(QUERY_REMOVE)
            conn.commit()
    return None

def clean_database():
    with sql.connect('data/data.db') as conn:
        q_remove = 'DELETE FROM weight'
        q_vacum = 'VACUUM'
        conn.execute(q_remove)
        conn.commit()
        conn.execute(q_vacum)
        conn.commit()
    return

def read_last_date():
    q = 'SELECT MAX(report_time) FROM weight'
    with sql.connect('data/data.db') as conn:
        result = conn.execute(q).fetchone()[0]
        return datetime.strptime(result, TIME_FORMAT) 

if __name__ == '__main__':
    # clean_database()
    # add_new_data(82.6)
    # print(remove_last_register('2021-11-09 19:27'))
    print(import_data())
    # print(create_new_data_dict(82.0))