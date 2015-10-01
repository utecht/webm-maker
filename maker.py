import win32gui
import os
import subprocess

import hotpy
import uploader
import namer


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
            'test-out.webm',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Encoding has started. This will take a while...")
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
                'test-out.avi'.format(title),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # out, err = PID.communicate()

    print("Capturing has begun. Press F9 again to stop!")

def stop_capture():
    global PID

    PID.terminate()
    PID.wait()

    name = '{}.webm'.format(namer.get_name())
    url = 'http://i.notabigtruck.com/i/tubes/{}'.format(name)

    print('Your url will be: {}'.format(url))

    encode_video()
    print('Uploading...')
    uploader.upload('test-out.webm', name)

    print('\n\n{}\n\n'.format(url))
    os.system('start {}'.format(url))
    

def handle_f9():
    global PID
    
    if PID is None:
        start_capture()
    else:
        stop_capture()


def main():
    hotpy.register(handle_f9, 'F9')
    hotpy.register(lambda: False, 'F9', ['Ctrl'])  # exit

    print("Press F9 to start recording!")

    hotpy.listen()

if __name__ == '__main__':
    main()
