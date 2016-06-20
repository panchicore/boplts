# python create_dirs "2013-01-01 TO 2017-01-01"

import sys, os
from datetime import datetime
from dateutil.rrule import rrule, DAILY

dates = sys.argv[1]

_from = datetime.strptime(dates.split(" TO ")[0], "%Y-%m-%d").date()
_to = datetime.strptime(dates.split(" TO ")[1], "%Y-%m-%d").date()

dirs = list(rrule(freq=DAILY, dtstart=_from, until=_to))

for i, dir in enumerate(dirs):
    path_dirs = os.path.join("fs", dir.strftime("%Y/%m/%d"))

    print path_dirs
    if not os.path.exists(path_dirs):
        os.makedirs(path_dirs)