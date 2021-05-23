from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

from app.utils import uart
from app.utils.tools import generate_time_rules_list

import time

import logging

# 用redis作任务持久化
jobstores = {'redis': RedisJobStore(db=1)}
executors = {'default': ThreadPoolExecutor(10),  # 默认线程数
            'processpool': ProcessPoolExecutor(3)}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)


class TimerWork:
    def __init__(self):
        scheduler.start()   # 启动定时任务进程
        uart.logger.warn('Timing task module started successfully.')


    def work_func(self, args):
        ds = 1 if args.get('DeviceStatus') else 0
        db = args.get('DeviceBrightness')
        db = (db // 20) if db else 0
        uart.send('post', 0, f"{ds}10{db}")


    def create_work(self, work_id, rules, args):
        rules = generate_time_rules_list(rules)
        work_id = str(work_id)
        scheduler.add_job(func=self.work_func, trigger='cron',
                          jobstore='redis', id=work_id,
                          year=rules[0], month=rules[1], day=rules[2],
                          hour=rules[3], minute=rules[4], second=rules[5],
                          day_of_week=int(rules[6])-1,
                          args=(args,), replace_existing=True)



    def delete_work(self, work_id):
        work_id = str(work_id)
        job = self.get_work(job_id=work_id)
        if not job:
            return
        job.remove()


    def editor_work(self, work_id, rules, args):
        job = self.get_work(job_id=work_id)
        if not job:
            return
        work_id = str(work_id)
        rules = generate_time_rules_list(rules)

        job.args = (args,)
        scheduler.reschedule_job(job_id=work_id, trigger='cron', jobstore='redis',
                                 year=rules[0], month=rules[1], day=rules[2],
                                 hour=rules[3], minute=rules[4], second=rules[5],
                                 day_of_week=int(rules[6])-1,)

    def get_works(self):
        work_list = scheduler.get_jobs()
        work_id_list = list()
        for work in work_list:
            work_id_list.append(int(work.id))
        return work_id_list


    def get_work(self, job_id):
        job = scheduler.get_job(job_id)
        return job


if __name__ == '__main__':
    # example...
    timer_work = TimerWork()
    timer_work.create_work('001', [2021, 4, 30, 10, 20, 0, 4], {
        'DeviceStatus': 1,
        'DeviceBrightness': 80
    })
    scheduler.start()
    while True:
        time.sleep(1)
