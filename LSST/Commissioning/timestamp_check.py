from datetime import datetime, timedelta
import sys

import papermill as pm
import yaml

import efd_utils

DATE_FORMAT = "%Y-%m-%d"
ONE_DAY = timedelta(days=1)

try:
    now = datetime.strptime(sys.argv[1], DATE_FORMAT)
except IndexError:
    now = datetime.now().date()
yesterday = now - ONE_DAY

with open(sys.argv[2]) as ifile:
    parameters = yaml.safe_load(ifile)
parameters["start_str"] = yesterday.strftime(DATE_FORMAT)
parameters["end_str"] = now.strftime(DATE_FORMAT)

csc_name = parameters["csc_name"]
if "=0" in csc_name:
    csc_name = csc_name.replace("=0", "")
else:
    csc_name = csc_name.replace("=", "_")

output_notebook = f"{csc_name}_{parameters['topic_name']}_{parameters['location']}_Timestamp_Check_{yesterday.strftime('%Y%m%d')}.ipynb"

pm.execute_notebook(
   'Timestamp_Check.ipynb',
   output_notebook,
   parameters=parameters
)