"""Модуль для подготовки csv к загрузке в Postgres"""

import datetime
import hashlib
import csv
import os


def process_row(i, val):
    val = val.replace('\0', '')
    transformed_val = val
    if i == 1:
        transformed_val = hashlib.md5(val.encode('utf-8')).hexdigest()
    elif i == 4:
        transformed_val = int(datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S').timestamp())
    if i in (1, 5, 6, 7, 8, 9, 10, 15, 17, 19):
        text_replaced = transformed_val.replace('"', '')
        transformed_val = f'"{text_replaced}"'
    return transformed_val


def csv_reader(file_name, sink_file_name):
    """
    Read a csv file
    """
    with open(file_name, 'r') as file_obj:
        reader = csv.reader((line.replace('\0', '') for line in file_obj), delimiter=',')
        with open(sink_file_name, 'w', encoding='utf-8') as sink_file_obj:
            sink_file_obj.write(
                f"{','.join([i for i in next(reader)])}\n"
            )
            for row in reader:
                sink_file_obj.write(
                    f"{','.join(map(str, [process_row(i, j) for i, j in enumerate(row)]))}\n"
                )


if __name__=='__main__':
    home_dir = '/usr/share/data_store/raw_data'
    file_name = 'win_users_events2.csv'
    sink_file_name = 'events.csv'

    csv_reader(
        os.path.join(home_dir, file_name),
        os.path.join(home_dir, sink_file_name))