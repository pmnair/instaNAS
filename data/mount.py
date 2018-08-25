import os
import sys
import glob
from pprint import pprint

class Mount(object):
    def __init__(s, conf="/proc/self/mounts"):
        s.mounts = []
        s.homes = []
        s.conf = conf
        s.refresh_mounts()

    def refresh_mounts(s):
        s.mounts = []
        with open(s.conf) as f:
            mounts = f.readlines()
            for m in mounts:
                mnt = {}
                i = m.split(' ')
                mnt['Device'] = i[0]
                mnt['Path'] = i[1]
                mnt['Filesystem'] = i[2]
                mnt['Options'] = i[3]
                s.mounts.append(mnt)

    def refresh_homes(s):
        s.homes = glob.glob("/home/*")

    def refresh(s):
        s.refresh_mounts()
        s.refresh_homes()
        #pprint(s.mounts)

    def is_dev_mounted(s, d):
        r = [m for m in s.mounts if m['Device'] == d]
        return (len(r) > 0)

    def get_dev_mounts(s, d):
        r = [m['Path'] for m in s.mounts if m['Device'] == d]
        return r

    def is_dir_mounted(s, d):
        r = [m for m in s.mounts if m['Path'] == d]
        return (len(r) > 0)

    def dev_contains_rootfs(s, d):
        r = [m['Path'] for m in s.mounts if d in m['Device']]
        if '/' in r:
            return True
        return False
