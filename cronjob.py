from datetime import datetime
from modules import cronjobs

for cronjob in cronjobs:
    obj = cronjob(None, None)

    now = datetime.now()

    print " > runnning %s cron job" %(obj.__class__.__name__)
    obj.cron(now)
