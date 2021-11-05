import sqlite3 as sql
from datetime import datetime, time, timedelta
import pandas as pd

TIME_FORMAT = '%Y-%m-%d %H:%M'
QUERY_SELECT = 'SELECT report_time, weight, who FROM weight'
QUERY_INSERT_DICT = '''
INSERT INTO weight (report_time, weight, who)
VALUES (:report_time, :weight, :who)
'''

def import_data() -> pd.DataFrame:
    with sql.connect('data/data.db') as conn:
        df = pd.read_sql(QUERY_SELECT, conn)
        return df

def read_last_date():
    q = 'SELECT MAX(report_time) FROM weight'
    with sql.connect('data/data.db') as conn:
        result = conn.execute(q).fetchone()[0]
        return datetime.strptime(result, TIME_FORMAT) 

def create_new_data_dict(weight: float, user: str ='Mateusz') -> dict:
    current_time_str =  datetime.now().strftime(TIME_FORMAT)
    new_data = {
        'report_time': current_time_str,
        'weight': weight,
        'who': user
    }
    return new_data

def create_new_data_dict_TEST(weight: float, user: str ='Mateusz') -> dict:
    last_time = read_last_date()
    new_time = last_time + timedelta(1) 
    current_time_str =  new_time.strftime(TIME_FORMAT)

    new_data = {
        'report_time': current_time_str,
        'weight': weight,
        'who': user
    }
    return new_data

def add_new_data(weight: float, user: str ='Mateusz'):
    # new_data_dict = create_new_data_dict(weight, user)
    new_data_dict = create_new_data_dict_TEST(weight, user)
    with sql.connect('data/data.db') as conn:
        conn.execute(QUERY_INSERT_DICT, new_data_dict)
        conn.commit()
    return 

def clean_database():
    with sql.connect('data/data.db') as conn:
        q_remove = 'DELETE FROM weight'
        q_vacum = 'VACUUM'
        conn.execute(q_remove)
        conn.commit()
        conn.execute(q_vacum)
        conn.commit()
    return

if __name__ == '__main__':
    # clean_database()
    # add_new_data(82.6)
    print(import_data())