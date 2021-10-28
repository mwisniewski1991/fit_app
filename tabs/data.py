import csv
import pandas as pd

def add_new_data(weight_dict):
    with open('data/weightdata.csv', mode='a') as csvfile:
        fieldnames = ['report_date', 'weight']
        weight_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        weight_writer.writerow(weight_dict)
        print('DONE')

def read_data():
    with open('data/weightdata.csv', 'r', ) as csvfile:
        _, *old_rows = csv.DictReader(csvfile, delimiter=',', lineterminator='\n', )
        for row in old_rows:
            print(row)

def import_data():
    return pd.read_csv('data/weightdata.csv')

if __name__ == '__main__':
    # add_new_data({'report_date':'2021-10-24', 'weight':80})
    # read_data()
    df = import_data()
    print(df)