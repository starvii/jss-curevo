from time import gmtime, strftime


def now():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())
