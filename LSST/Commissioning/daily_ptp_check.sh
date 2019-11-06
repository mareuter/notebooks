#!/bin/bash
if [ $# -lt 1 ]; then
  echo "Usage: daily_ptp_check.sh <date string>"
  exit 255
fi
check_date=$1

python ptp_check_run.py ${check_date}
python ptp_check_run.py ${check_date} ATCamera wreb 0.1
python ptp_check_run.py ${check_date} ScriptQueue
python ptp_check_run.py ${check_date} ATSpectrograph
