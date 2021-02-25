import datetime


def inform(message, finalize=False):
    now = datetime.datetime.now()
    date_time = "Date Time: " + str(now.day) + "/" + str(now.month) + "/" + str(now.year) + " " + str(now.hour) + ":" + str(
                now.minute) + ":" + str(now.second)
    print(message)
    print(date_time)

    if finalize:
        exit(-1)
