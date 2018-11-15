def flip_array(flips, exposure):
    fx, fy = flips
    array = exposure.getMaskedImage().getImage().clone().getArray()
    if fx:
        array = numpy.flip(array, axis=1)
    if fy:
        array = numpy.flip(array, axis=0)
    return array

def orient_amps(image):
    
    detector = image.getDetector()
    
    # for the geometry we've chosen, the y=0 amps are in the top
    # Normally the read corner would tell you this, but there is currently a bug
    flipXY = {'C00':(False, True),
              'C01':(False, True),
              'C02':(False, True),
              'C03':(False, True),
              'C04':(False, True),
              'C05':(False, True),
              'C06':(False, True),
              'C07':(False, True),
              'C10':(True, False),
              'C11':(True, False),
              'C12':(True, False),
              'C13':(True, False),
              'C14':(True, False),
              'C15':(True, False),
              'C16':(True, False),
              'C17':(True, False)}
    
    amp_sections = {}
    
    for channel_name, flips in flipXY.items():
        amp_sections[channel_name] = {}
        bbox = detector[channel_name].getRawHorizontalOverscanBBox()
        amp_sections[channel_name]['horizontal_overscan'] = flip_arrays(flips, raw[bbox])
        bbox = detector[channel_name].getRawVerticalOverscanBBox()
        amp_sections[channel_name]['vertical_overscan'] = flip_arrays(flips, raw[bbox])
        bbox = detector[channel_name].getRawDataBBox()
        amp_sections[channel_name]['image'] = flip_arrays(flips, raw[bbox])
        bbox = detector[channel_name].getRawPrescanBBox()
        amp_sections[channel_name]['prescan'] = flip_arrays(flips, raw[bbox])

    return amp_sections