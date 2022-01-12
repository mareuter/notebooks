import asyncio

import numpy as np
import pandas as pd

async def calculate_statistics(day_obs, seq_num, butler):
    dataId = {"instrument": "LATISS", "detector": 0,
              "exposure.day_obs": day_obs, "exposure.seq_num": seq_num}
    raw = butler.get('raw', dataId)
    amps = raw.getDetector()
    amp_medians = [np.median(raw[amps[i].getRawDataBBox()].image.array) for i in range(len(amps))]
    return amp_medians

async def make_image_dataframe(day_obs, seq_num, butler):
    columns = [f"Amp{i:02}" for i in range(16)]
    ccd_medians = await asyncio.gather(*[calculate_statistics(day_obs, seq_num, butler)])
    return pd.DataFrame(ccd_medians, columns=columns)