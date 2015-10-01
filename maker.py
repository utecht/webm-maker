import win32gui
import os
import subprocess

import hotkey
import uploader


def cleanup():
    try:
        os.unlink('test-out.avi')
        os.unlink('test-out.webm')
    except FileNotFoundError:
        pass

def encode_video():
    p = subprocess.Popen('ffmpeg\\ffmpeg.exe '
            '-i test-out.avi '
            '-c:v libvpx -b:v 10000k '
            'test-out.webm')
    p.wait()


def get_rect(hwnd):
    x, y, x2, y2 = win32gui.GetWindowRect(hwnd)
    w = x2 - x
    h = y2 - y

    return x, y, w, h

def get_title(hwnd):
    return win32gui.GetWindowText(hwnd)


PID = None

def start_capture():
    global PID


    window = win32gui.GetForegroundWindow()
    title = get_title(window)

    cleanup()
    PID = subprocess.Popen('ffmpeg\\ffmpeg.exe -f gdigrab -i title="{}" '
                '-framerate 15 -vf "scale=\'iw/2\':-1" '
                '-c:v rawvideo -pix_fmt yuv420p '
                'test-out.avi'.format(title))

def stop_capture():
    global PID

    PID.terminate()
    PID.wait()

    encode_video()
    uploader.upload('test-out.webm', 'test.webm')



hotkey.register(start_capture, 'F9')
hotkey.register(stop_capture, 'F8')
hotkey.register(lambda: False, 'F9', ['Ctrl'])
hotkey.listen()
