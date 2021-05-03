from django.shortcuts import HttpResponse
from django.views.decorators.http import require_http_methods
from app.models import Lighting_Usage_Record, Lighting_Timer_Work_Queues
from django.db.models import Sum
from datetime import timedelta, date
from app.utils import uart
from app.utils.rewrite import DateEncoder
from app.utils.tools import generate_duration_dict, timer_work_add_key
from app.utils.schedule import TimerWork

import json
import time

# 开启定时任务监听线程
timer_work = TimerWork()


@require_http_methods(["GET", "POST"])
def intelligent_light_device_control_api(request):
    content = {"errorCode": 200, "statusText": "OK", "data": ''}
    if request.method == 'POST':
        form_data = json.loads(request.body.decode('utf-8'))
        send_data = '0003'
        if form_data:
            send_data = ''.join([str(data) for data in form_data.values()])
        uart.send('post', 0, send_data)
    else:
        params = request.GET.get('params')
        if params:
            uart.send('get', params, '')
            all_status = ''
            start_run_time = time.time()
            while not all_status:
                all_status = uart.redis_conn.get('LORA_RECEIVE_ALL_STATUS_DATA')
                run_time = time.time() - start_run_time
                if run_time > 3:
                    content['errorCode'] = 204
                    content['statusText'] = 'No content returned'
                    break
            uart.redis_conn.delete('LORA_RECEIVE_ALL_STATUS_DATA')
            content['data'] = all_status or ''
    content = json.dumps(content)
    return HttpResponse(content=content, status=200, content_type="application/json")


@require_http_methods(["GET"])
def intelligent_light_data_analysis_api(request):
    content = {"errorCode": 200, "statusText": "OK", "data": ''}
    if request.method == 'GET':
        params = request.GET.get('params')
        data = list()
        if params == "week_use_duration_statistics":
            date_to = date.today()
            date_from = date.today() - timedelta(days=6)
            result = Lighting_Usage_Record.objects \
                .values('RecordTime') \
                .filter(RecordTime__range=(date_from, date_to), DeviceName='ILD001') \
                .annotate(sum_duration=Sum('Duration'))
            data = list(result)
        data = generate_duration_dict(data)
        content['data'] = data
    content = json.dumps(content, cls=DateEncoder)
    return HttpResponse(content=content, status=200, content_type="application/json")


@require_http_methods(["GET", "POST"])
def intelligent_light_timer_task_manage_api(request):
    content = {"errorCode": 200, "statusText": "OK", "data": ''}
    if request.method == 'GET':
        params = request.GET.get('params')
        if params == "timer_work_queues":
            result = list(Lighting_Timer_Work_Queues.objects.all().values())
            data = timer_work_add_key(result)
            content['data'] = data
    if request.method == 'POST':
        form_data = json.loads(request.body.decode('utf-8'))
        delete_key = form_data.get('delete_key')
        if not delete_key:
            key = form_data.get('key')
            work_number = form_data['WorkNumber'] or -1
            del form_data['WorkNumber'], form_data['CreateTime']
            if key:
                del form_data['key']
                db = Lighting_Timer_Work_Queues \
                    .objects \
                    .create(**form_data)
                db.save()
                timer_work.create_work(db.WorkNumber, db.TimeRules,
                    form_data)
            else:
                db = Lighting_Timer_Work_Queues.objects \
                    .filter(WorkNumber=work_number) \
                    .update(**form_data)
                db.save()
                timer_work.editor_work(db.WorkNumber, db.TimeRules,
                    form_data)
        else:
            Lighting_Timer_Work_Queues.objects \
                .filter(WorkNumber=delete_key).delete()
            timer_work.delete_work(delete_key)

    content = json.dumps(content, cls=DateEncoder)
    return HttpResponse(content=content, status=200, content_type="application/json")
