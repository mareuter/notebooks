import argparse
import asyncio
import os
import sys
from lsst.ts import salobj

async def main(opts):
    async with salobj.Domain() as domain:
        csc = salobj.Remote(domain=domain, name=opts.csc, index=opts.index)
        await csc.start_task

        await salobj.set_summary_state(csc, getattr(salobj.State, opts.state), settingsToApply=opts.settings)
        

if __name__ == "__main__":

    name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(prog=name, description="Change states")
    
    parser.add_argument("csc", help="CSC to change states.")
    parser.add_argument("state", help="State to change to.")
    parser.add_argument("--index", dest="index", help="CSC index")
    parser.add_argument("--settings", dest="settings", help="CSC settings")
    
    args = parser.parse_args()
    
    asyncio.run(main(args))