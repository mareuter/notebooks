from datetime import datetime, timedelta
import os
import subprocess
import sys

import papermill as pm

DATE_FORMAT = "%Y-%m-%d"
ONE_DAY = timedelta(days=1)
NBCONVERT_CONFIG = "nbconvert_config.py"
OUTPUT_DIR = "reports"

try:
    now = datetime.strptime(sys.argv[1], DATE_FORMAT)
except IndexError:
    now = datetime.now().date()
yesterday = now - ONE_DAY

try:
    csc_name = sys.argv[2]
except IndexError:
    csc_name = "ATHeaderService"
    
try:
    topic_name = sys.argv[3]
except IndexError:
    topic_name = "logevent_heartbeat"

try:
    frequency = eval(sys.argv[4])
except IndexError:
    frequency = 1

output_notebook = f'PTP_Check_{csc_name}_{topic_name}_{yesterday.strftime("%Y%m%d")}.ipynb'
output_html = output_notebook.replace('ipynb', 'html')

pm.execute_notebook(
   'PTP_Check.ipynb',
   output_notebook,
   parameters=dict(csc_name=csc_name, topic_name=topic_name,
                   frequency=frequency,
                   start_str=yesterday.strftime(DATE_FORMAT),
                   end_str=now.strftime(DATE_FORMAT))
)

subprocess.run(["jupyter", "nbconvert", "--config", NBCONVERT_CONFIG,
                "--output-dir", OUTPUT_DIR, output_notebook])

while True:
    if os.path.exists(os.path.join(OUTPUT_DIR, output_html)):
        os.remove(output_notebook)
        break
    