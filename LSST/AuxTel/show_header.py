import sys

import lsst.afw.cameraGeom.utils as cameraGeomUtils
import lsst.afw.display as afwDisplay
import lsst.daf.persistence as dafPersist

expId = int(sys.argv[1])

dataPath = "/lsstdata/offline/teststand/NCSA_auxTel/gen2repo"
butler = dafPersist.Butler(dataPath)
dataId = dict(expId=expId)

raw = butler.get('raw', dataId)
header = raw.getInfo().getMetadata().toDict()
for value in header.items():
    print(value)