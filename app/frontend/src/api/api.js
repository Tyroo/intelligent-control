import {
  get, post, del, put,
} from '@/request/request';

/** ****** 登录-退出请求Api ******* */
export const clickUserLogin = (data) => post('/LoginApi', data);
export const clickUserLogout = (data) => post('/LogoutApi', data);
/** ****** 照明设备 ********** */

// 发送设备状态更改POST请求
export const deviceStatusChange = (data) => post('/IntelligentLighting/DeviceControlApi/', data);
// 获取设备当前全部状态GET请求
export const getDeviceAllStatus = (data) => get('/IntelligentLighting/DeviceControlApi/', data);
// 获取周设备使用时长GET请求
export const getWeekUseDuration = (data) => get('/IntelligentLighting/DataAnalysisApi/', data);
// 获取定时任务队列GET请求
export const getTimerWorkQueues = (data) => get('/IntelligentLighting/TimerTaskManageApi/', data);
// 更改定时任务项POST请求
export const changeTimerWorkTerms = (data) => post('/IntelligentLighting/TimerTaskManageApi/', data);
// 删除定时任务项post请求
export const deleteTimerWorkTerms = (data) => post('/IntelligentLighting/TimerTaskManageApi/', data);
