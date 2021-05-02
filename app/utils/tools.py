from datetime import timedelta, date, datetime


def generate_duration_dict(data: list) -> dict:
    duration = dict()
    if data:
        data_times = [datetime.strftime(d.get('RecordTime'), '%Y-%m-%d') for d in data]
        for _day in range(0, 7):
            day = str(date.today() - timedelta(_day))
            try:
                index = data_times.index(day)
                duration[day] = round(data[index].get('sum_duration') / 60, 1)
            except ValueError:
                duration[day] = 0
    return duration


def timer_work_add_key(data: list) -> list:
    for d in data:
        key = d.get('key', d['WorkNumber'])
        d['key'] = key
    return data or []


def generate_time_rules_list(time_rules):
    time_rules = time_rules[1:-1]
    time_rules = time_rules.split(',')
    if len(time_rules) == 7:
        return time_rules
    new_time_rules = []
    for i in range(7):
        try:
            if time_rules[i] == '*':
                new_time_rules.insert(i, time_rules[i])
            else:
                new_time_rules.insert(i, int(time_rules[i]))
        except IndexError:
            new_time_rules.insert(i, '*')
    return new_time_rules
