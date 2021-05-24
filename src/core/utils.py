from datetime import datetime, timedelta


def prepare_date_time_field(value: str):
    if 'PM' not in value:
        return value.strip(' AM')

    date = datetime.strptime(value.strip(' PM'), "%m/%d/%Y %H:%M")
    pm_date = timedelta(hours=12)
    clean_date = date + pm_date
    return clean_date.strftime("%m/%d/%Y %H:%M")
