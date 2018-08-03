import os
import sys
import glob
import signal
import logging
import pyudev
import platform
import subprocess

class System(object):
    def __init__(s):
        r=subprocess.check_output("lscpu", stderr=subprocess.STDOUT, shell=False)
        t1=r.strip('\n').split('\n')
        s.cpu_info = {}
        for i in t1:
            t2 = i.split(':')
            if len(t2) > 1:
                s.cpu_info[t2[0]] = t2[1].lstrip()
        p = platform.uname()
        s.os = p[0]
        s.hostname = p[1]
        s.kversion = p[2]
        s.arch = p[4]
        p = platform.linux_distribution()
        s.distro = p[0].title() + " (" + p[1] + ")"

    def os_info(s):
        return s.os + " " + s.distro + " Kernel:" + s.kversion
    def uptime(s):
        r=subprocess.check_output(["/usr/bin/uptime", "-p"], stderr=subprocess.STDOUT, shell=False)
        return r.strip('\n')

    def num_cpus(s):
        return s.cpu_info['CPU(s)']

    def cpu(s):
        return s.cpu_info['Model name'] + " " + s.cpu_info['CPU(s)'] + " Core(s)"
