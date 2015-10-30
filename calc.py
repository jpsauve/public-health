# -*- coding: utf-8 -*-
"""Module to load data from file and produce pandas dataframes.

__author__      = "Jacques Sauve"
"""

import json
import csv
import numpy as np
import pandas as pd
from datetime import datetime

def read_json(data_file, columns):
    with open(data_file) as f:
        data = json.load(f)
    df = pd.DataFrame(data, columns=columns)
    df['Day'] = df['TimeStamp'].map(lambda x: datetime.strftime(
        datetime.strptime(x['$date'][:19], '%Y-%m-%dT%H:%M:%S'), '%Y-%m-%d'))
    return df

def read_csv(filename, key):
    entries = {}
    with open(filename) as f:
        csv_reader = csv.DictReader(f, delimiter=',', quotechar='"')
        for row in csv_reader:
            try:
                for col in row:
                    if col and row[col]:
                        row[col] = row[col].decode('utf-8')
            except Exception, ex:
                print 'Decode error, col', col
                pass
            entries[row[key]] = row
    return entries

def insert_neighborhood(df, filename, key):
    neighborhood_map = read_csv(filename, key)
    df['Neighborhood'] = df['LocationKey'].map(lambda x: neighborhood_map[x]['nome'] if x in neighborhood_map else 'Unknown')
    return df

def daily_volume(df):
    # there must be a better way to do this: need to study pandas more
    result = pd.DataFrame(df['Day'].value_counts().sort_index())
    return result

def by_location(df):
    filter = df[df['Neighborhood'] != 'Unknown']
    result = filter['Neighborhood'].value_counts()
    return result
