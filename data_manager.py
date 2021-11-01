import sqlite3 as sql
from datetime import datetime 
import pandas as pd

TIME_FORMAT = '%Y-%m-%d %H:%M'
QUERY_SELECT = 'SELECT report_time, weight, who FROM weight'
QUERY_INSERT_DICT = '''
INSERT INTO weight (report_time, weight, who)
VALUES (:report_time, :weight, :who)
'''

def import_data() -> pd.DataFrame:
    with sql.connect('data/data.db') as conn:
        return pd.read_sql(QUERY_SELECT, conn)

def create_new_data_dict(weight: float, user: str ='Mateusz') -> dict:
    current_time_str =  datetime.now().strftime(TIME_FORMAT)
    new_data = {
        'report_time': current_time_str,
        'weight': weight,
        'who': user
    }
    return new_data

def add_new_data(weight: float, user: str ='Mateusz') -> None:
    new_data_dict = create_new_data_dict(weight, user)
    with sql.connect('data/data.db') as conn:
        conn.execute(QUERY_INSERT_DICT, new_data_dict)
        conn.commit()
    return 

def clean_database() -> None:
    with sql.connect('data/data.db') as conn:
        q_remove = 'DELETE FROM weight'
        q_vacum = 'VACUUM'
        conn.execute(q_remove)
        conn.commit()
        conn.execute(q_vacum)
        conn.commit()
    return



if __name__ == '__main__':
    # add_new_data({'report_date':'2021-10-24', 'weight':80})
    # read_data()
    # df = import_data()
    clean_database()
    # add_new_data(81.5)
    # add_new_data(82.5)
    # add_new_data(83.5)
    # print(import_data())