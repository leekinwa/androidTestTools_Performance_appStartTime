# -*- coding: utf-8 -*-

import time, os, platform

# 判断系统平台;
if platform.system() == 'Windows':
    seek = 'findstr'
else:
    seek = 'grep'

# 获取activity;
def getActivity():
    activity = os.popen('adb shell dumpsys activity top | ' + seek + ' ACTIVITY').readline().split()[1]
    # print activity
    return activity

# 计算启动速度;
def appStart():
    runCount = 1
    appStart_fristTime = []
    appStart_secondTime = []
    activity1 = getActivity()
    print activity1
    while runCount <= 20:
        if runCount <= 10:
            totalTime_frist = os.popen('adb shell am start -S -W -n ' + activity1 + ' | ' + seek + ' TotalTime').readline().split(':')[1]
            print u'首次启动, 第%d次:' %runCount, totalTime_frist
            # print totalTime_frist
            appStart_fristTime.append(int(totalTime_frist))
        else:
            totalTime_second = os.popen('adb shell am start -W -n ' + activity1 + ' | ' + seek + ' TotalTime').readline().split(':')[1]
            print u'二次启动, 第%d次' %int(runCount-10), totalTime_second
            # print totalTime_second
            appStart_secondTime.append(int(totalTime_second))
        time.sleep(0.5)
        os.system('adb shell input keyevent 4')
        while True:
            activity2 = getActivity()
            if activity2 == activity1 and 'launcher' not in activity2:
                os.popen('adb shell input keyevent 4')
            else:
                break
        runCount += 1

    appStart_fristTime_avg = sum(appStart_fristTime) / len(appStart_fristTime)
    appStart_secondTime_avg = sum(appStart_secondTime) / len(appStart_secondTime)
    print u'首次启动平均耗时: %d, 最大值: %d' %(appStart_fristTime_avg, max(appStart_fristTime))
    print u'二次启动平均耗时: %d, 最大值: %d' %(appStart_secondTime_avg, max(appStart_secondTime))

if __name__ == '__main__':
    if platform.system() == 'Windows':
        logCount_input = raw_input('请启动被测应用, 启动后按enter继续: '.decode('utf-8').encode('gbk'))
    else:
        logCount_input = raw_input('请启动被测应用, 启动后按enter继续: ')
    appStart()