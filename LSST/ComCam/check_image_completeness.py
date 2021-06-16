import argparse
import asyncio

from astropy.time import Time, TimeDelta

from lsst_efd_client import EfdClient

async def main(opts):
    efd_name = "ldf_stable_efd"
    client = EfdClient(efd_name)
    
    obs_beg = Time(f"{opts.check_date}T12:00", scale="tai")
    delta = TimeDelta(24*3600.0, format="sec", scale="tai")
    obs_end = obs_beg + delta
    
    start_int_df = await client.select_time_series("lsst.sal.CCCamera.logevent_startIntegration", "imageName",
                                                   obs_beg, obs_end)
    
    print(f"Date: {opts.check_date}")
    if start_int_df.size == 0:
        print("No images found!")
    else:
        num_images = start_int_df.count()[0]
        
        img_oods_df = await client.select_time_series("lsst.sal.CCArchiver.logevent_imageInOODS", "obsid,sensor",
                                                      obs_beg, obs_end)
        if img_oods_df.size == 0:
            print(f"Total images: {num_images}")
            print("No images in OODS!")
        else:
            oods_images = img_oods_df.groupby("obsid").count()
            
            bad_images = oods_images.index[oods_images.sensor != 9]
            
            # Find images that have no sensors in OODS
            missing_images = []
            for image_name in start_int_df.imageName.array:
                if image_name not in oods_images.index:
                    missing_images.append(image_name)
            
            if opts.show_missing:  
                # Find images that do not have all 9 sensors in OODS
                some_missing_images = []
                standard_sensors = set(["S00", "S01", "S02", "S10", "S11", "S12", "S20", "S21", "S22"])
                for image_name in bad_images:
                    #print(image_name)
                    sensors = img_oods_df.sensor[img_oods_df.obsid == image_name].array
                    sensor_set = set([f"S{x}" for x in sensors])
                    #print(sensor_set)
                    missing_sensors = standard_sensors.difference(sensor_set)
                    some_missing_images.append((image_name, sorted(missing_sensors)))
                    
            print("Summary")
            print(f"Total images: {num_images}")
            print(f"Images some missing sensors: {bad_images.size}")
            print(f"Images missing all sensors: {len(missing_images)}")
            print(f"Percentage of bad images: {(((bad_images.size + len(missing_images))/num_images)*100):.2f}%")
            if opts.show_missing:
                print("Images Missing All Sensors")
                for image_name in missing_images:
                    print(image_name)
                print("Images Missing Some Sensors")
                for image_name, missing_sensors in some_missing_images:
                    sensor_str = ":".join(missing_sensors)
                    print(f"{image_name}   {sensor_str}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("check_date", help="The date to check for image completeness.")
    parser.add_argument("-m", "--show-missing", action="store_true", help="List the images missing sensors.")
    
    args = parser.parse_args()
    asyncio.run(main(args))