#!/usr/bin/python

import subprocess

def res_cmd_lfeed(cmd):
    return subprocess.Popen(
        cmd, stdout=subprocess.PIPE,
        shell=True).stdout.readlines()

def res_cmd_no_lfeed(cmd):
    return [str(x).rstrip("\n") for x in res_cmd_lfeed(cmd)]

def main():
    cmd = ("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits")
    gpus = res_cmd_no_lfeed(cmd)
    print(res_cmd_no_lfeed(cmd))
    cmdFan = ("nvidia-smi --query-gpu=fan.speed --format=csv,noheader,nounits")
    fans = res_cmd_no_lfeed(cmdFan)
    print(res_cmd_no_lfeed(cmdFan))

    for i, gpu in enumerate(gpus):
        if (int(gpu) > 60):
            print('GPU'+str(i)+' - TOO HOT!')
            targetFanNum = i * 2
            targetFanSpeed = int(max(min(100,round(int(fans[i])+10, -1)),0))
            print('targetFanNum'+str(targetFanNum))
            print('targetFanSpeed'+str(targetFanSpeed))
            cmdGpuChange1 = ("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [gpu:"+str(i)+"]/GPUFanControlState=1")
            result=res_cmd_no_lfeed(cmdGpuChange1)
            cmdFanChange1 = ("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [fan:"+str(targetFanNum)+"]/GPUTargetFanSpeed="+str(targetFanSpeed))
            result=res_cmd_no_lfeed(cmdFanChange1)
            cmdFanChange2 = ("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [fan:"+str(targetFanNum+1)+"]/GPUTargetFanSpeed="+str(targetFanSpeed))
            result=res_cmd_no_lfeed(cmdFanChange2)
        elif (int(gpu) < 55):
            print('GPU'+str(i)+' - fan speed can be decreased.')
            targetFanNum = i * 2
            targetFanSpeed = int(max(min(100,round(int(fans[i])-10, -1)),0))
            print('targetFanNum'+str(targetFanNum))
            print('targetFanSpeed'+str(targetFanSpeed))
            cmdGpuChange1 = ("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [gpu:"+str(i)+"]/GPUFanControlState=1")
            result=res_cmd_no_lfeed(cmdGpuChange1)
            cmdFanChange1 = ("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [fan:"+str(targetFanNum)+"]/GPUTargetFanSpeed="+str(targetFanSpeed))
            result=res_cmd_no_lfeed(cmdFanChange1)
            cmdFanChange2 = ("DISPLAY=:0 XAUTHORITY=/var/run/lightdm/root/:0 nvidia-settings -a [fan:"+str(targetFanNum+1)+"]/GPUTargetFanSpeed="+str(targetFanSpeed))
            result=res_cmd_no_lfeed(cmdFanChange2)
        else:
            print('GPU'+str(i)+' is stable.')

if __name__ == '__main__':
    main()
