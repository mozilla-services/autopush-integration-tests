from datetime import datetime


DIFF_ALLOWED = 3 * 60  # 3 minutes (in case of clock skew)


def utc_to_timestamp(time_utc):
    """ Normalize UTC string then convert to timestamp. """
    t = str(time_utc)
    if 'Z' in t:
        t = t.replace('Z', '')
    if 'T' in t:
        t = t.replace('T', ' ')
    if '.' in t:
        t = t.split('.')[0]
    return datetime.strptime(str(t), "%Y-%m-%d %H:%M:%S").strftime('%s')


def verify_timeout(test_start, sentry_log_time):
    """ Verify Sentry log time is within acceptable time
    delta from test start"""

    ts_test_start = utc_to_timestamp(test_start)
    ts_sentry_log_time = utc_to_timestamp(sentry_log_time)

    # take abs value to allow for some clock skew
    diff_actual = abs((int(ts_test_start) - int(ts_sentry_log_time)))

    if diff_actual < DIFF_ALLOWED:
        return True
    else:
        return False
