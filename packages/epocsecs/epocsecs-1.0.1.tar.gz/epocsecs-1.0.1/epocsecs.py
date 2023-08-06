from datetime import datetime

import sys

import os

VERSION = '1.0.1'


def safe_call(cast_to,cast_what,default=None):
    """
    attempt to call a cast_method, with an object to cast, in the event of failure it returns the default value

    :param cast_to: the method or casting to call
    :param cast_what: the object to cast
    :param default: what to return in the case that the casting fails
    :return: the cast object or the default object if an exception occures durring casting
    """
    try:
        return cast_to(cast_what)
    except Exception as e:
        return default


def get_date(base_dt):
    """
    convert something that may or maynot be a datetime to a datetime

    :param base_dt: our object to convert (string/int/or datetime)
    :return: datetime
    """
    if isinstance(base_dt,datetime):
        return base_dt
    if isinstance(base_dt,basestring):
        dt = safe_call(int, base_dt, safe_call(float, base_dt, base_dt))
        if isinstance(dt,basestring):
            from dateutil.parser import parse as date_parse
            dt = date_parse(dt)
    else:
        dt = base_dt
    if isinstance(dt,(int,float)):
        try:
            date_potentials = [datetime.fromordinal(dt),datetime.fromtimestamp(dt)]
            dt = min(date_potentials,key=lambda dx:abs(datetime.now()-dx).total_seconds())
        except:
            dt = datetime.fromtimestamp(dt)
    if not isinstance(dt,datetime):
        raise ValueError("Unable To Convert %r to a datetime"%base_dt)
    return dt

def epocsecs(target_date=None,base_dt="1/1/2000"):
    """
    calculate the epoc seconds for any base epoc_date

    :param target_date: the date to convert to epocsecs (default now)
    :param base_dt: the epoc base_date (ie number of seconds since this date) (default=1/12000)
    :return: float (seconds between target_date and epoc_date)
    """
    if target_date is None:
        target_date=datetime.now()
    else:
        target_date = get_date(target_date)
    base_dt = get_date(base_dt)
    return (target_date-base_dt).total_seconds()


def parse_args():
    """
    execute based on command line arguments... just prints to stdout

    :return: None
    """
    import argparse
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]))
    parser.add_argument("-t", "--target", help="SEE: target_date")
    parser.add_argument("-e", "--epoc", help="SEE: epoc_date")
    parser.add_argument("target_date", nargs="?", default=None, help="The Target date(default=now) to convert")
    parser.add_argument("epoc_date", nargs="?", default="1/1/2000", help="The Epoc date(default=1/1/2000) to use")
    args = parser.parse_args()
    epoc = args.epoc or args.epoc_date
    target = args.target or args.target_date
    print epocsecs(target, epoc)

if __name__ == "__main__":
    parse_args()