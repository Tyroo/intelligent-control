from datetime import timedelta, date, datetime
from app.models import Lighting_Usage_Record
from django.conf import settings

import jwt


# 生成近七天设备使用时长字典数据
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


# 将定时任务视图函数查询后的数据中加入key键，以满足前端之需
def timer_work_add_key(data: list) -> list:
    for d in data:
        key = d.get('key', d['WorkNumber'])
        d['key'] = key
    return data or []


# 将前端提交的时间规则表单项转化为cron格式
def generate_time_rules_list(time_rules: str) -> list:
    time_rules = time_rules[1:-1]
    time_rules = time_rules.split(',')
    new_time_rules = list()

    if len(time_rules) == 7:
        return time_rules
    for i in range(7):
        try:
            if time_rules[i] == '*':
                new_time_rules.insert(i, time_rules[i])
            else:
                new_time_rules.insert(i, int(time_rules[i]))
        except IndexError:
            new_time_rules.insert(i, '*')
    return new_time_rules


def create_lighting_usage_record(create_dict: dict):
    Lighting_Usage_Record.objects.create(**create_dict)


def generate_token(username: str) -> jwt:
    # 构造header
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    # 构造payload
    payload = {
        'usr': username,
        'exp': datetime.now() + timedelta(days=5)
    }

    salt = settings.__getattribute__('SECRET_KEY')

    jwt_result = jwt.encode(headers=headers, key=salt, payload=payload, algorithm='HS256')
    return jwt_result


def token_to_username(token: str) -> str:
    token = jwt.decode(token, settings.__getattribute__('SECRET_KEY'),
                       algorithms=['HS256'])
    token_user = token.get('usr')
    return token_user
