import pyudev
import subprocess
import time
from pprint import pprint

class Drives(object):
    def __init__(s, mnt):
        s.udev = pyudev.Context()
        s.mnt = mnt

    def mount(s, dev, path):
        try:
            if s.mnt.is_dir_mounted(path):
                path += "_{0}".format(int(time.time()))
            r=subprocess.check_output(["mkdir", "-p", path], stderr=subprocess.STDOUT, shell=False)
            r=subprocess.check_output(["mount", dev, path, "-o", "rw"], stderr=subprocess.STDOUT, shell=False)
            return True
        except subprocess.CalledProcessError as e:
            print(e)
            return False

    def unmount(s, dev):
        try:
            if s.mnt.is_dev_mounted(dev):
                r=subprocess.check_output(["umount", dev], stderr=subprocess.STDOUT, shell=False)
            return True
        except subprocess.CalledProcessError as e:
            print(e)
            return False

    def list(s):
        drives = []
        s.mnt.refresh()

        for d in s.udev.list_devices(subsystem='block', DEVTYPE='disk'):
            if 'ID_TYPE' not in d or d.get('ID_TYPE') != 'disk':
                continue
            drv = {'FileSystem': 'None', 'Model': 'Unknown',
                    'Serial': 'Unknown', 'Label': '',
                    'MountPath': 'None'}
            drv['Path'] = d.device_node
            if 'ID_FS_TYPE' in d:
                drv['FileSystem'] = d.get('ID_FS_TYPE')
            if 'ID_FS_LABEL' in d:
                drv['Label'] = d.get('ID_FS_LABEL')
            if 'ID_MODEL' in d:
                drv['Model'] = d.get('ID_MODEL')
            if 'ID_SERIAL_SHORT' in d:
                drv['Serial'] = d.get('ID_SERIAL_SHORT')
            if s.mnt.is_dev_mounted(d.device_node):
                drv['MountPath'] = s.mnt.get_dev_mounts(d.device_node)
            parts = []
            for p in d.children:
                part = {'FileSystem': 'None', 'Label': '',
                        'MountPath': 'None'}
                part['Path'] = p.device_node
                if 'ID_FS_TYPE' in p:
                    part['FileSystem'] = p.get('ID_FS_TYPE')
                if 'ID_FS_LABEL' in p:
                    part['Label'] = p.get('ID_FS_LABEL')

                if s.mnt.is_dev_mounted(p.device_node):
                    part['MountPath'] = s.mnt.get_dev_mounts(p.device_node)
                parts.append(part)
            drv['Partitions'] = parts
            drives.append(drv)
        #pprint(drives)
        return drives
