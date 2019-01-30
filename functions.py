import ctypes
import getpass
import logging as log
import os
import platform
import webbrowser
from threading import Thread

import psutil
import pyautogui
import pythoncom
import wmi
from mss import mss
from pygame import cdrom
from uptime import uptime
from win32com.client import Dispatch

import key_listener as kl
import tray
from file_manager import FileManager

_tray_icon = None
_FileManager = FileManager()

INCORRECT_MSG = 'Niepoprawny PIN.'
CORRECT_MSG = 'Poprawny PIN.'


def create_icon_tray(pin):
    global _tray_icon
    _tray_icon = tray.create_icon(pin)


def start_main_loop():
    tray.main_loop()


# Info ########################################################

def get_static_info():
    cpu_name = platform.processor()
    freq = psutil.cpu_freq()
    system_info = platform.uname()
    is64 = platform.machine().endswith('64')
    if is64:
        architecture = '64 bit'
    else:
        architecture = '32 bit'

    data = {
        'cpuName': cpu_name,
        'coreCount': psutil.cpu_count(logical=False),
        'coreCountLogical': psutil.cpu_count(),
        'minFreq': freq.min,
        'maxFreq': freq.max,
        'system': system_info.system,
        'release': system_info.release,
        'version': system_info.version,
        'architecture': architecture,
        'uptime': uptime()
    }
    log.debug('data={}'.format(data))
    return data


def get_fast_interval_info():
    usage = psutil.cpu_percent()
    freq = psutil.cpu_freq().current
    data = {
        'usagePercent': usage,
        'currentFreq': freq
    }
    log.debug('data={}'.format(data))
    return data


def get_slow_interval_info():
    memory = psutil.virtual_memory()
    battery = psutil.sensors_battery()
    try:
        battery_percent = battery.percent
        battery_power_plugged = battery.power_plugged
        battery_secsleft = battery.secsleft
    except AttributeError:
        battery_percent = 0.0
        battery_power_plugged = True
        battery_secsleft = 0
    data = {
        'totalMemory': memory.total,
        'availableMemory': memory.available,
        'percentMemory': memory.percent,
        'usedMemory': memory.used,
        'freeMemory': memory.free,

        'percentBattery': battery_percent,
        'powerPlugged': battery_power_plugged,
        'secondsLeftBattery': battery_secsleft
    }
    log.debug('data={}'.format(data))
    return data


def get_short_info():
    p = platform.uname()
    data = {
        'system': "{} {}".format(p.system, p.release),
        'user': getpass.getuser()
    }
    log.debug('data={}'.format(data))
    return data


def get_disk_info():
    data = []
    for disk in psutil.disk_partitions():
        usage = psutil.disk_usage(disk.mountpoint)
        data.append((disk.mountpoint, disk.fstype, usage.total, usage.used, usage.free, usage.percent))
    log.debug('data={}'.format(data))
    return data


# Regulation #################################################

def set_volume(up):
    if up:
        vol_btn = 'volumeup'
    else:
        vol_btn = 'volumedown'
    pyautogui.press(vol_btn)
    data = {
        'param': vol_btn
    }
    log.debug('data={}'.format(data))
    return data


def set_brightness(value):
    pythoncom.CoInitialize()
    wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(value, 0)
    data = {
        'param': str(value)
    }
    log.debug('data={}'.format(data))
    return data


# ON OFF #####################################################

def shutdown(delay, restart, cancel):
    # delay = str(delay)
    if not cancel:
        if not restart:
            shut_msg = 'shutdown /t {} /s'.format(delay)
            msg_val = os.system(shut_msg)
            if msg_val is not 0:
                msg = 'Zamykanie zostało już zlecone.'
            else:
                if delay > 0:
                    msg = 'Zamykanie za: {} sekund.'.format(delay)
                else:
                    msg = 'Zamykanie rozpoczęte.'
            data = {'param': msg}
            log.debug('data={}, delay={}'.format(data, delay))
            return data
        else:
            shut_msg = 'shutdown /t {} /r /f'.format(delay)
            msg_val = os.system(shut_msg)
            if msg_val is not 0:
                msg = 'Zamykanie zostało już zlecone.'
            else:
                if delay > 0:
                    msg = 'Restartowanie za: {} sekund.'.format(delay)
                else:
                    msg = 'Restartowanie rozpoczęte.'
            data = {'param': msg}
            log.debug('data={}, delay={}'.format(data, delay))
            return data
    else:
        shut_msg = 'shutdown /a'
        msg_val = os.system(shut_msg)
        if msg_val is not 0:
            msg = 'Nie zaplanowano żadnego zamykania.'
        else:
            msg = 'Anulowano zamykanie.'
        data = {'param': msg}
        log.debug('data={}'.format(data))
        return data


# File manager ################################################

def get_file_manager():
    global _FileManager
    return _FileManager


# Additional ##################################################

def open_cd_rom():
    try:
        cdrom.init()
        cd = cdrom.CD(0)
        cd.init()
        cd.eject()
        cd.quit()
        cdrom.quit()
        msg = "CD-ROM Otwarty."
    except Exception:
        msg = "Nie masz CD-ROM'u."

    data = {'param': msg}
    log.debug('data={}'.format(data))
    return data


def open_internet_browser(page):
    if page == '':
        page = 'google.pl'
    webbrowser.open(page, new=2)

    data = {'param': page}
    log.debug('data={}'.format(data))
    return data


def screenshot():
    with mss() as s:
        s.shot(mon=1)
    with open('monitor-1.png', 'rb') as img:
        data = {'content': img.read()}
        log.debug('data={}'.format(data))
        return data


def get_key_logs():
    logs = kl.get_keys()
    data = {'param': logs}
    log.debug('data={}'.format(data))
    return data


def start_key_listener():
    pass


def open_info_window(text, title, is_notif):
    if not is_notif:
        Thread(target=ctypes.windll.user32.MessageBoxW, args=(0, text, title, 4096)).start()
    else:
        _tray_icon.ShowBalloon(title, text, 5000)
    data = {'param': 'Wyświetlam <{}: {}>'.format(title, text)}
    log.debug('data={}'.format(data))
    return data


def say(speech):
    pythoncom.CoInitialize()
    syn = Dispatch('SAPI.SpVoice')
    system_msg = syn.Speak(speech)
    data = {'param': speech}
    log.debug('data={}, system_msg={}'.format(data, system_msg))
    return data


def click(arrow):
    if arrow.startswith('hotkey'):
        clicked_btn = arrow.split('.')[1:]
        pyautogui.hotkey(*clicked_btn)
    else:
        pyautogui.press(arrow)

    data = {
        'param': '+'.join(arrow.split('.'))
    }
    log.debug('data={}'.format(data))
    return data
