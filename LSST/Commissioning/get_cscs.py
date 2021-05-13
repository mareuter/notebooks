import argparse
import asyncio
import csv

from lsst_efd_client import EfdClient


async def main(opts):
    client = EfdClient(opts.efd_name)
    measurements = await client.get_topics()
    cscs = []
    for measurement in measurements:
        try:
            csc = measurement.split(".")[2]
            cscs.append(csc)
        except IndexError:
            pass
    cscs = set(cscs)
    cscs = sorted(cscs)

    filename = opts.efd_name.replace("_efd", "")
    with open(f"{filename}_cscs.csv", "w") as ofile:
        writer = csv.writer(ofile)
        writer.writerow(cscs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("efd_name", help="Provide the EFD to query")

    args = parser.parse_args()

    asyncio.run(main(args))
