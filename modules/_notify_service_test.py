from erina import Handler, NotifyService, TextNotification


class NotifyServiceTest(Handler):

    def cron(self, time):
        time = time.strftime("%H:%M")
        time_check = time.split(":")

        if 1:
            notifier = NotifyService()
            notifier.send(TextNotification("notificacion %s" %(time)))
            print "\tnotifying time... OK"

        else:
            print "\tnotifying time... FALSE"
