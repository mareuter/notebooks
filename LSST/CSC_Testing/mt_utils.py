from astropy.coordinates import AltAz, ICRS, EarthLocation, Angle
from astropy.time import Time
import astropy.units as u

from lsst.ts import salobj

def altaz_to_radec(alt, az):
    location = EarthLocation.from_geodetic(
            lon=-70.747698 * u.deg, lat=-30.244728 * u.deg, height=2663.0 * u.m
    )

    current_time = salobj.astropy_time_from_tai_unix(salobj.current_tai())
    current_time.location = location

    coord_frame_radec = ICRS()

    alt_az = AltAz(az=Angle(az, unit=u.deg), alt=Angle(alt, unit=u.deg), location=location,
                   obstime=current_time)

    return alt_az.transform_to(coord_frame_radec)

async def slew(ptg, mount, stop_tracking=False):
    print("Slewing Telescope")
    ack = await ptg.cmd_raDecTarget.start(timeout=30.)
    print(f"ack={ack.ack} ack.error={ack.error}, ackcmd.result={ack.result}")
    while True:
        in_position = await mount.evt_axesInPosition.next(flush=False, timeout=60.)
        print(f"State: {in_position.elevation}, {in_position.azimuth}")
        if in_position.elevation and in_position.azimuth:
            print("Telescope in position.")
            break

    if stop_tracking:
        ack = await ptg.cmd_stopTracking.start(timeout=30.)
        print("Stop Tracking")
        print(f"ack={ack.ack} ack.error={ack.error}, ackcmd.result={ack.result}")