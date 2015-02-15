from __future__ import print_function
from . import censusname as cn

# In the absence of tests, as least make sure specifying arguments doesn't break anything:
_C = cn.Censusname('{given} {surname}', cn.NAMEFILES, cn.MAX_FREQUENCIES, csv_args={'delimiter': ','})

print(_C.generate())
