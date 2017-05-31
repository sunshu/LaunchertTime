#/usr/bin/python
#encoding:utf-8
import csv
import os
import time


class App(object):
    def __init__(self):
        self.content = ""
        self.startTime = 0

    #启动App
    def LaunchApp(self):
        cmd = 'adb shell am start -W -n com.android.browser/.BrowserActivity'
        self.content=os.popen(cmd)

    #停止App
    def StopApp(self):
        cmd = 'adb shell am force-stop com.android.browser'
        #cmd = 'adb shell input keyevent 3'
        os.popen(cmd)

    #获取启动时间
    def GetLaunchedTime(self):
        for line in self.content.readlines():
            if "ThisTime" in line:
                self.startTime = line.split(":")[1]
                break
        return self.startTime

#控制类
class Controller(object):
    def __init__(self, count):
        self.app = App()
        self.counter = count
        self.alldata = [("timestamp", "elapsed")]

    #单次测试过程
    def testprocess(self):
        self.app.LaunchApp()
	time.sleep(2)
        elapsedtime =  self.app.GetLaunchedTime()
        self.app.StopApp()
	time.sleep(2)
        currenttime = self.getCurrentTime()
        self.alldata.append((currenttime,elapsedtime))

    #多次执行
    def run(self):
        while self.counter >0:
            self.testprocess()
            self.counter = self.counter - 1
    
#获取当前的时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        return currentTime


    #保存的数据
    def saveDataToCSV(self):
        csvfile = file('startTime.csv','wb')
        writer = csv.write(csvfile)
        writer.writerows(self.alldata)
        csvfile.close()


if __name__ == "__main__":
    controll = Controller(10)
    controll.run()
    controll.saveDataToCSV()
