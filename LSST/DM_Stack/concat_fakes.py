from astropy.table import Table, vstack

def create_concat(band_filter, xmin, xmax, ymin, ymax):
    loaddir = '/scratch/nate2/ic_fakes_only'
    savedir = '/project/mreuter/ic_fakes_cat'
    table_list = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            try:
                infile = os.path.join(loaddir, '{}_{},{}.fits.fits'.format(band_filter, x, y))
                hdulist = fits.open(infile)
                print(infile)
            except FileNotFoundError:
                continue
            table_list.append(Table(hdulist[1].data))
    table = vstack(table_list)
    table.write(os.path.join(savedir, "{}_{}-{},{}-{}.fits".format(band_filter, xmin, xmax, ymin, ymax)), overwrite=True)