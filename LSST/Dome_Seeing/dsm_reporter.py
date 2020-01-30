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
    file_path = sys.argv[1]
except IndexError:
    file_path = os.path.expanduser("~/Dropbox_LSST/Dome_Seeing_Monitor/DSM_Data")
    
try:
    date_str = sys.argv[2]
except IndexError:
    date_str = "20200129_134503"

try:
    csc_index = int(sys.argv[3])
except IndexError:
    csc_index = 1

output_notebook = f'DSM_Report_{date_str}.ipynb'
output_html = output_notebook.replace('ipynb', 'html')

pm.execute_notebook(
   'DSM_Report.ipynb',
   output_notebook,
   parameters=dict(ipath=file_path, date_str=date_str, csc_index=csc_index)
)

subprocess.run(["jupyter", "nbconvert", "--config", NBCONVERT_CONFIG,
                "--output-dir", OUTPUT_DIR, output_notebook])

#while True:
#    if os.path.exists(os.path.join(OUTPUT_DIR, output_html)):
#        os.remove(output_notebook)
#        break