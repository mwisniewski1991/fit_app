import sqlite3 as sql
from datetime import datetime, time, timedelta
import pandas as pd

TIME_FORMAT = '%Y-%m-%d %H:%M'
QUERY_SELECT = 'SELECT report_time, part_of_day, weight, who FROM weight'
QUERY_INSERT_DICT = '''
INSERT INTO weight (report_time, part_of_day, weight, who)
VALUES (:report_time, :part_of_day, :weight, :who)
'''

def import_data() -> pd.DataFrame:
    with sql.connect('data/data.db') as conn:
        df = pd.read_sql(QUERY_SELECT, conn)
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

def read_last_date():
    q = 'SELECT MAX(report_time) FROM weight'
    with sql.connect('data/data.db') as conn:
        result = conn.execute(q).fetchone()[0]
        return datetime.strptime(result, TIME_FORMAT) 

if __name__ == '__main__':
    # clean_database()
    print(import_data())
    # add_new_data(82.6)
    # print(create_new_data_dict(82.0))