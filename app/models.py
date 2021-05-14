from django.db import models


# 智能照明-设备使用记录
class Lighting_Usage_Record(models.Model):
    id = models.AutoField(primary_key=True)             # 主键
    DeviceName = models.CharField(max_length=50)        # 设备名
    OpenTime = models.DateTimeField()                   # 开始使用的时刻
    CloseTime = models.DateTimeField()                  # 使用结束的时刻
    Duration = models.IntegerField()                    # 使用了多长时间，单位（秒）
    RecordTime = models.DateField(auto_now_add=True)    # 生成这条记录的时刻


# 智能照明-定时任务调度
class Lighting_Timer_Work_Queues(models.Model):
    WorkNumber = models.AutoField(primary_key=True)   # 主键
    WorkContent = models.CharField(max_length=200)    # 任务内容
    DeviceStatus = models.BooleanField()              # 设备状态
    DeviceBrightness = models.IntegerField()          # 设备亮度
    TimeRules = models.CharField(max_length=80)       # 时间规则
    CreateTime = models.DateField(auto_now_add=True)  # 创建时间
