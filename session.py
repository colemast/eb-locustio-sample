import random

import testdata

import user
import settings

random.seed(settings.RANDOM_SEED)

USERS = list(user.UserFactory().generate(settings.NUM_USERS))

class SessionFactory(testdata.DictFactory):
	u = testdata.RandomSelection(USERS)
	mida_session_id = testdata.RandomLengthStringFactory(10, 10)
	was_session_id = testdata.RandomLengthStringFactory(8, 8)
