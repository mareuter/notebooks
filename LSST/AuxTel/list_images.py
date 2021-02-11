import csv
import warnings

import lsst.daf.persistence as dafPersist


def list_at_images(date_filter, butler_path="/project/shared/auxTel", from_seqnum=None, save_file=False):
    """Create catalog of AuxTel images.
    
    Functions to parse a Butler instance and write an image information
    catalog. The currently collected information is:
    
    Exposure Date, Sequence Number, Object Name, Image Type,
    Exposure Time, Filter, Grating
    
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
    dfilter = dict(dayObs=date_filter)
    images = butler.queryMetadata('raw', ['dayObs', 'seqnum', 'expId'], dfilter)
    print(f"Number of Images: {len(images)}")
    titles = ["ExpDate", "SeqNum", "Object", "ImgType", "ExpTime", "Filter", "Grating"]
    print("\t".join(titles))
    ofile = None
    if save_file:
        ofilename = f"images_{date_filter.replace('-', '')}.csv"
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
        for image in images:
            seqnum = image[1]
            if from_seqnum is not None and seqnum <= from_seqnum:
                continue
            dataId = dict(**dfilter, seqnum=seqnum)
            raw = butler.get('raw', dataId)
            header = raw.getInfo().getMetadata().toDict()
            info = [header['DATE-OBS'], str(seqnum), str(header['OBJECT']), header['IMGTYPE'],
                    str(header['EXPTIME']), header['FILTER'], header['GRATING']]
            print("\t".join(info))
            if save_file:
                writer.writerow(info)