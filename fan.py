#!/usr/bin/python

import os
import subprocess
import datetime

def res_cmd_lfeed(cmd):
    return subprocess.Popen(
        cmd, stdout=subprocess.PIPE,
        shell=True).stdout.readlines()

def res_cmd_no_lfeed(cmd):
    return [str(x).rstrip("\n") for x in res_cmd_lfeed(cmd)]

def writeLog(message):
    with open('/autofan.log', mode='a') as flog:
        flog.write('\n'+message)
    print(message)

def main():
    # outputs date/time
    dt_now = datetime.datetime.now()
    writeLog(dt_now.strftime('%Y%m%d %H:%M:%S'))

    # prep log file
    if (os.path.exists('/autofan.log')):
        writeLog('Log file size='+str(os.path.getsize('/autofan.log')))
        if (os.path.getsize('/autofan.log') > 1048):
            for i in range(10000):
                if (os.path.exists('/autofan.'+str(i)+'.log') == false):
                    os.rename('/autofan.log', 'autofan.'+str(i)+'log')
                    break

    with open('/fan_config.txt') as f:
        line = f.readline()
        writeLog('config file (/fan_config) was loaded.')
        values=line.split(' ')
        writeLog('targetTempUpper='+str(values[0]+' targetTempBottom='+str(values[1])))
    cmd = ("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits")
    gpus = res_cmd_no_lfeed(cmd)
    writeLog(",".join(gpus))
    cmdFan = ("nvidia-smi --query-gpu=fan.speed --format=csv,noheader,nounits")
    fans = res_cmd_no_lfeed(cmdFan)
    writeLog(",".join(fans))

    if (len(gpus) == 0):
        result=res_cmd_no_lfeed("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [gpu:"+str(i)+"]/GPUFanControlState=0")
        writeLog("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [gpu:"+str(i)+"]/GPUFanControlState=0")

    for i in range(len(gpus)*2):
        if (fans[i].isdigit() == false):
            writeLog("Fan["+str(i)+"] returned ERR! => rebooting...")
            result = res_cmd_no_lfeed("reboot now")

    for i, gpu in enumerate(gpus):
        if (int(gpu) > int(values[0])):
            writeLog('GPU'+str(i)+' - TOO HOT!')
            targetFanNum = i * 2
            targetFanSpeed = int(max(min(100,round(int(fans[i])+10, -1)),40))
            writeLog('targetFanNum'+str(targetFanNum))
            writeLog('targetFanSpeed'+str(targetFanSpeed))
            cmdGpuChange1 = ("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [gpu:"+str(i)+"]/GPUFanControlState=1")
            result=res_cmd_no_lfeed(cmdGpuChange1)
            writeLog(cmdGpuChange1)
            cmdFanChange1 = ("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [fan:"+str(targetFanNum)+"]/GPUTargetFanSpeed="+str(targetFanSpeed))
            result=res_cmd_no_lfeed(cmdFanChange1)
            writeLog(cmdFanChange1)
            cmdFanChange2 = ("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [fan:"+str(targetFanNum+1)+"]/GPUTargetFanSpeed="+str(targetFanSpeed))
            result=res_cmd_no_lfeed(cmdFanChange2)
            writeLog(cmdFanChange2)
        elif (int(gpu) < int(values[1])):
            writeLog('GPU'+str(i)+' - fan speed can be decreased.')
            targetFanNum = i * 2
            targetFanSpeed = int(max(min(100,round(int(fans[i])-10, -1)),40))
            writeLog('targetFanNum'+str(targetFanNum))
            writeLog('targetFanSpeed'+str(targetFanSpeed))
            cmdGpuChange1 = ("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [gpu:"+str(i)+"]/GPUFanControlState=1")
            result=res_cmd_no_lfeed(cmdGpuChange1)
            writeLog(cmdGpuChange1)
            cmdFanChange1 = ("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [fan:"+str(targetFanNum)+"]/GPUTargetFanSpeed="+str(targetFanSpeed))
            result=res_cmd_no_lfeed(cmdFanChange1)
            writeLog(cmdFanChange1)
            cmdFanChange2 = ("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [fan:"+str(targetFanNum+1)+"]/GPUTargetFanSpeed="+str(targetFanSpeed))
            result=res_cmd_no_lfeed(cmdFanChange2)
            writeLog(cmdFanChange2)
        else:
            writeLog('GPU'+str(i)+' is stable.')

if __name__ == '__main__':
    main()
