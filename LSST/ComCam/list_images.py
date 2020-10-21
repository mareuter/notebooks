import csv
import operator
import warnings

import lsst.daf.persistence as dafPersist


def list_cc_images(date_filter, butler_path="/lsstdata/offline/teststand/NCSA_comcam/gen2repo",
                   is_ccs=False, from_seqnum=None, save_file=False):
    """Create catalog of ComCam images.
    
    Functions to parse a Butler instance and write an image information
    catalog. The currently collected information is:
    
    Exposure Date, Sequence Number, Object Name, Image Type,
    Exposure Time, Filter
    
    This information can be written into a file by using the save_file
    parameter. The created file is named images_YYYYMMDD.csv.
    
    One can append to the file by using the from_seqnum parameter and
    passing it the last sequence number found previously.
    
    Attributes
    ----------
    date_filter : str
        Date to filter on in YYYY-MM-DD format.
    butler_path : str
        Path to Butler containing the relevant files.
    from_seqnum : int, optional
        Only list images after this number.
    save_file : bool, optional
        Create a CSV file with the image catalog information.
    """

    butler = dafPersist.Butler(butler_path)
    dfilter = dict(dayObs=date_filter, detector=4)
    images = butler.queryMetadata('raw', ['dayObs', 'seqnum', 'expId', 'detector'], dfilter)
    print(f"Number of Images: {len(images)}")
    if is_ccs:
        titles = ["ExpDate", "SeqNum", "ImgType", "TestType", "ExpTime"]#, "Filter"]
    else:
        titles = ["ExpDate", "SeqNum", "Object", "ImgType", "TestType", "ExpTime"]#, "Filter"]
    print("\t".join(titles))
    ofile = None
    if save_file:
        if is_ccs:
            head = "ccs"
        else:
            head = "arc"
        ofilename = f"{head}_images_{date_filter.replace('-', '')}.csv"
        if from_seqnum is None:
            mode = 'w'
        else:
            mode = 'a'
        ofile = open(ofilename, mode, newline='')
        writer = csv.writer(ofile)
        if from_seqnum is None:
            writer.writerow(titles)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        infos = []
        for image in images:
            seqnum = image[1]
            if from_seqnum is not None and seqnum <= from_seqnum:
                continue
            dataId = dict(**dfilter, seqnum=seqnum)
            try:
                raw = butler.get('raw', dataId)
                header = raw.getInfo().getMetadata().toDict()
                if is_ccs:
                    info = (header['DATE-OBS'], seqnum, header['IMGTYPE'],
                            header['TESTTYPE'], header['EXPTIME'])#, header['FILTER']]
                else:
                    info = (header['DATE-OBS'], seqnum, str(header['OBJECT']), header['IMGTYPE'],
                            header['TESTTYPE'], header['EXPTIME'])#, header['FILTER']]
                #print("\t".join(info))
                infos.append(info)
            except Exception:
                print(f"Skipping image {seqnum}")
        infos.sort(key=operator.itemgetter(1))
        if save_file:
            for info in infos:
                writer.writerow(info)