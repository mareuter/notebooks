import collections
from datetime import datetime, timedelta
import os

import aioinflux

Token = collections.namedtuple("Token", ["uname", "pwd"])
CSC = collections.namedtuple("CSC", ["name", "index"])

AVAILABLE_EFDS = {"summit": "summit-influxdb-efd.lsst.codes",
                  "tucson": "test-influxdb-efd.lsst.codes"}

QUERY_BASE = "SELECT {columns} FROM \"efd\".\"autogen\".\"lsst.sal.{csc}.{topic}\""
QUERY_TIME_RANGE = "{time_column} >= \'{start}\' AND {time_column} <= \'{end}\'"
QUERY_LAST_TIME = "ORDER BY {time_column} DESC LIMIT {limit}"

def get_client(which_efd):
    efd_url = AVAILABLE_EFDS[which_efd]
    token = get_token(which_efd)
    return aioinflux.InfluxDBClient(host=efd_url,
                                    port=443,
                                    ssl=True,
                                    username=token.uname,
                                    password=token.pwd,
                                    db='efd',
                                    output="dataframe")

def get_token(which_efd):
    token_file = os.path.join(os.path.expanduser("~/"), f".{which_efd}_efd")
    with open(token_file, 'r') as fd:
        uname = fd.readline().strip()  # Can't hurt to be paranoid
        pwd = fd.readline().strip()
    return Token(uname, pwd)

def get_base_query(columns, csc_name, topic_name, csc_index=0, ):
    query_columns = ",".join(columns)
    if csc_index:
        query_columns += f",{csc_name}ID"
    
    query = QUERY_BASE.format(columns=query_columns, csc=csc_name, topic=topic_name)
    if csc_index:
        query += f" WHERE {csc_name}ID = {csc_index}"
        
    return query

def get_time_clause(time_column="time", last=False, limit=1, date_range=None):
    query = ""
    if last:
        query += QUERY_LAST_TIME.format(time_column=time_column, limit=limit)
    else:
        if date_range is None:
            last = datetime.utcnow()
            first = last - timedelta(1, "day")
        else:
            first, last = date_range
        
        query += QUERY_TIME_RANGE.format(time_column=time_column, start=first, end=last)
        
    return query

def filter_measurements(measurements, csc_name, topic_name):
    csc_filtered = [measurement.split('.')[-1] for measurement in measurements['name'].values if csc_name in measurement]
    topic_filtered = [topic for topic in csc_filtered if topic_name in topic]
    return topic_filtered

def get_cscs(csc_file):
    cscs = []
    with open(csc_file, 'r') as ifile:
        for line in ifile:
            v = line.strip()
            cscs.append(parse_csc(v))
        
    return cscs

def parse_csc(csc_str):
    if '=' in csc_str:
        parts = csc_str.split('=')
        return CSC(parts[0], int(parts[1]))
    else:
        return CSC(csc_str, 0)