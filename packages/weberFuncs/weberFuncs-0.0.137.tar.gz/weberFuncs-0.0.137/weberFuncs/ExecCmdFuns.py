#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__createTime__ = "2017/9/7 11:42"
__author__ = "WeiYanfeng"
__email__ = "weber.juche@gmail.com"
__version__ = "0.0.1"
        
~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
对调用命令函数进行简化封装。
参考
[Python subprocess.Popen Examples](https://www.programcreek.com/python/example/50/subprocess.Popen)
[Python带timeout的命令执行_redice's Blog](http://www.redicecn.com/html/Python/20120906/434.html)
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from WyfPublicFuncs import PrintTimeMsg, PrintInline, PrintAndSleep
import time
import subprocess as sp
# import threading


def ExecCmdWaitByPopen(sCmd):
    # 通过 Popen 调用命令，等待模式
    # import psutil
    PrintTimeMsg("ExecCmdWaitByPopen(%s)..." % sCmd)
    tmBegin = time.time()
    # iRet = os.system(sCmd)
    p = sp.Popen(sCmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    while True:
        sLine = p.stdout.readline()
        if sLine == "":
            break
        sLine = sLine.strip()
        if isinstance(sLine, unicode):
            PrintInline('  %s\n' % sLine)
        else:
            PrintInline('  %s\n' % sLine.decode('gbk'))  # 可以不要.encode('utf8')
    out, err = p.communicate()  # 阻塞，直至子进程结束
    PrintTimeMsg("ExecCmdWaitByPopen.out=(%s)" % out)
    PrintTimeMsg("ExecCmdWaitByPopen.err=(%s)" % err)
    tmLast = time.time() - tmBegin
    PrintTimeMsg("ExecCmdWaitByPopen(%s)=(%s).Consume=%.2fs!" % (sCmd, p.returncode, tmLast))
    return p.returncode


def ExecCmdWaitOutErrByPopen(sCmd):
    # 通过 Popen 调用命令，等待模式, 并返回标准输出和标准错误输出结果
    # import psutil
    PrintTimeMsg("ExecCmdWaitByPopen(%s)..." % sCmd)
    tmBegin = time.time()
    # p = sp.Popen(sCmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    p = sp.Popen(sCmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)  # echo 命令要求 shell=True
    lsOut = p.stdout.readlines()
    lsErr = p.stderr.readlines()
    out, err = p.communicate()  # 阻塞，直至子进程结束
    # PrintTimeMsg("ExecCmdWaitByPopen.out=(%s)" % out)
    # PrintTimeMsg("ExecCmdWaitByPopen.err=(%s)" % err)
    if lsOut:
        PrintTimeMsg("    STDOUT=>>%s<<" % ''.join(lsOut))
    if lsErr:
        PrintTimeMsg("    STDERR=>>%s<<" % ''.join(lsErr))
    tmLast = time.time() - tmBegin
    PrintTimeMsg("ExecCmdWaitByPopen(%s)=(%s).Consume=%.2fs!" % (sCmd, p.returncode, tmLast))
    return p.returncode, lsOut, lsErr


def ExecCmdTimeOutByPopen(sCmd, iTimeOutSecs):
    # 通过 Popen 调用命令，带超时参数，等待模式, 并返回标准输出和标准错误输出结果
    # import psutil
    PrintTimeMsg("ExecCmdTimeOutByPopen(%s)..." % sCmd)
    tmBegin = time.time()
    # p = sp.Popen(sCmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    p = sp.Popen(sCmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=False)
    # 若 shell=True ，则无法超时
    bTimeOut = False
    while True:
        if p.poll() is not None:
            break
        iPassSecs = time.time() - tmBegin
        if iTimeOutSecs > 0 and iPassSecs > iTimeOutSecs:
            bTimeOut = True
            p.terminate()
        PrintAndSleep(0.1, "JustForSleep", False)
    lsOut = p.stdout.readlines()
    lsErr = p.stderr.readlines()
    if lsOut:
        PrintTimeMsg("    STDOUT=>>%s<<" % ''.join(lsOut))
    if lsErr:
        PrintTimeMsg("    STDERR=>>%s<<" % ''.join(lsErr))
    tmLast = time.time() - tmBegin
    sTimeOutHint = 'TimeOut!' if bTimeOut else ''
    PrintTimeMsg("ExecCmdTimeOutByPopen(%s)=(%s).Consume=%.2fs!%s" % (
        sCmd, p.returncode, tmLast, sTimeOutHint))
    return p.returncode, lsOut, lsErr


def tryExecCmdByPopen():
    # ExecCmdTimeOutByPopen('ffprobe -v error -print_format json -show_format -show_streams "D:\\AudioVideo\\ts\\CCTV1_20171124-175932.014.ts"', 5)
    # return
    # ExecCmdWaitByPopen('ping 127.0.0.1')
    # ExecCmdWaitByPopen('ping www.qq.com')
    # ExecCmdWaitByPopen('ping www.qq.com -t')
    # ExecCmdWaitOutErrByPopen('ping www.qq.com')
    ExecCmdWaitOutErrByPopen('echo www.qq.com')
    ExecCmdWaitOutErrByPopen('echo www.\nqq.com 1>&2')
    ExecCmdTimeOutByPopen('ping www.qq.com -t', 10)
    ExecCmdTimeOutByPopen('ping www.qq.com', 10)


# --------------------------------------
if __name__ == '__main__':
    tryExecCmdByPopen()
