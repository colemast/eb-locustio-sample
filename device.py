import testdata

import settings


class DeviceFactory(testdata.DictFactory):
    device_id = testdata.RandomLengthStringFactory(14, 14)
    device_type = testdata.StatisticalValuesFactory([('Desktop', settings.PERC_DESKTOP),
                                              ('iOS', settings.PERC_IOS), 
                                              ('Android', settings.PERC_ANDROID),
                                              ('Mobile Browser', settings.PERC_MOBILE_BROWSER),
                                              ('Tablet Browser', settings.PERC_TABLET_BROWSER)])
