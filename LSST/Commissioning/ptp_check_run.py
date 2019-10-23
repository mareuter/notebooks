from datetime import datetime, timedelta

import papermill as pm

DATE_FORMAT = "%Y-%m-%d"
ONE_DAY = timedelta(days=1)

now = datetime.now().date()
yesterday = now - ONE_DAY

pm.execute_notebook(
   'PTP_Check.ipynb',
   f'PTP_Check_{yesterday.strftime("%Y%m%d")}.ipynb',
   parameters=dict(start_str=yesterday.strftime(DATE_FORMAT),
                   end_str=now.strftime(DATE_FORMAT))
)