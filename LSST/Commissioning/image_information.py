import argparse
import operator

import lsst.daf.butler as dafButler

def main(opts):
    data_repo = "/repo/main"
    butler = dafButler.Butler(data_repo,
                              collections=[f"{opts.instrument}/raw/all"], 
                              instrument=opts.instrument)

    where_clause = [f"exposure.day_obs={opts.day_obs}",
                    f"exposure.seq_num>={opts.seq_start}",
                    f"exposure.seq_num<={opts.seq_end}"]
    
    selection = " and ".join(where_clause)# + " order by exposure.seq_num"
    
    records = butler.registry.queryDimensionRecords('exposure', where=selection)
    records = sorted(records, key=operator.attrgetter("seq_num"))

    if opts.show_first_record:
        print(list(records)[0])
    
    for record in records:
        output = []
        output.append(f"{record.seq_num}")
        output.append(f"{record.observation_type}")
        output.append(f"{record.exposure_time}")
        output.append(f"{record.physical_filter}")
        print("\t".join(output))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("instrument")
    parser.add_argument("day_obs")
    parser.add_argument("seq_start")
    parser.add_argument("seq_end")
    
    parser.add_argument("--show-first-record", action="store_true")
    
    args = parser.parse_args()
    main(args)