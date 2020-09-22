import argparse
import os
import subprocess

from astropy.time import Time
import papermill as pm
import yaml

DATE_FORMAT = "%Y%m%d_%H%M"
NBCONVERT_CONFIG = "nbconvert_config.py"
OUTPUT_DIR = "reports"

def main(opts):

    if not os.path.exists(os.path.join(OUTPUT_DIR, opts.database)):
        os.mkdir(os.path.join(OUTPUT_DIR, opts.database))

    with open(opts.config) as ifile:
        info = yaml.safe_load(ifile)
    topic = info["tablename"]
    parts = topic.split(".")
    csc_name = parts[2]
    topic_name = parts[3].split('_')[-1]
    try:
        csc_index = ":" + str(info["cscIndex"])
    except KeyError:
        csc_index = ""
    start_time = Time(opts.start_time, scale="tai")
    end_time = Time(opts.end_time, scale="tai")
    start_time_fmt = start_time.strftime(DATE_FORMAT)
    end_time_fmt = end_time.strftime(DATE_FORMAT)

    output_notebook = f"{csc_name}{csc_index}_{topic_name}_S{start_time_fmt}_E{end_time_fmt}.ipynb"
    output_html = output_notebook.replace('ipynb', 'html')

    pm.execute_notebook(
        'Diagnostics.ipynb',
        output_notebook,
        parameters=dict(ifilename=opts.config, efd_name=opts.database,
                        start_time_str=opts.start_time, end_time_str=opts.end_time)
    )

    subprocess.run(["jupyter", "nbconvert", "--config", NBCONVERT_CONFIG,
                    "--output-dir", os.path.join(OUTPUT_DIR, opts.database),
                    output_notebook])

    #while True:
    #    if os.path.exists(os.path.join(OUTPUT_DIR, opts.database, output_html)):
    #        os.remove(output_notebook)
    #        break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-d", "--database", dest="database", help="The EFD to get the data from")
    parser.add_argument("-c", "--config", dest="config", help="Provide the YAML configuration file")
    parser.add_argument("start_time", help="Set the query start time (TAI) in ISO8601 format")
    parser.add_argument("end_time", help="Set the query end time (TAI) in ISO8601 format")

    args = parser.parse_args()

    main(args)
