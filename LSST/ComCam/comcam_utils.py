import asyncio

import numpy as np
import pandas as pd

async def calculate_statistics(day_obs, seq_num, detector, butler):
    dataId = {"instrument": "LSSTComCam", "detector.raft": "R22", "detector.id": detector,
              "exposure.day_obs": day_obs, "exposure.seq_num": seq_num}
    raw = butler.get('raw', dataId)
    amps = raw.getDetector()
    amp_medians = [np.median(raw[amps[i].getRawDataBBox()].image.array) for i in range(len(amps))]
    amp_medians.insert(0, detector)
    return amp_medians

async def make_image_dataframe(day_obs, seq_num, butler):
    columns = [f"Amp{i:02}" for i in range(16)]
    columns.insert(0, "DetId")
    ccd_medians = await asyncio.gather(*[calculate_statistics(day_obs, seq_num, i, butler) for i in range(9)])
    return pd.DataFrame(ccd_medians, columns=columns)