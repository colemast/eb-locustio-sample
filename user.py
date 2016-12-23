import random

import testdata

import settings
import device

random.seed(settings.RANDOM_SEED)

DEVICES = list(device.DeviceFactory().generate(settings.NUM_DEVICES))

class UserFactory(testdata.DictFactory):
    party_id = testdata.RandomLengthStringFactory(8, 8)
    devices = testdata.RandomLengthListFactory(testdata.RandomSelection(DEVICES),
        settings.MIN_NUM_DEVICES_PER_USER, settings.MAX_NUM_DEVICES_PER_USER)