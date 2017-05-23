import datetime


def assign(value, default):
    if value is None:
        return default
    return value


def set_null_if_blank(my_dict):
    my_dict = { k:v.strip() for k, v in my_dict.iteritems()}
    return dict(map(lambda (k, v): (k, None) if v == "" else (k, v), my_dict.iteritems()))


def is_valid_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False