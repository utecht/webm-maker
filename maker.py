import win32gui
import win32api
import os
import subprocess
import progressbar
import signal

import hotpy
import uploader
import namer


def feed_file_to_handle_with_progress(filename, handle):
    chunk_size = 1024
    position = 0
    total = os.path.getsize(filename)

    widgets = [progressbar.Percentage(), ' ',
               progressbar.Bar(), ' ',
               progressbar.ETA(), ' ',
               progressbar.FileTransferSpeed()]
    bar = progressbar.ProgressBar(widgets=widgets, maxval=total)
    bar.start()

    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                handle.close()
                bar.finish()
                break
            handle.write(chunk)
            position += len(chunk)
            bar.update(position)



def cleanup():
    try:
        os.unlink('test-out2.avi')
        os.unlink('test-out.webm')
    except FileNotFoundError:
        pass

def encode_video():
    p = subprocess.Popen('ffmpeg\\ffmpeg.exe '
            '-i - '
            '-c:v libvpx -b:v 10000k '
            'test-out.webm',
            bufsize=64,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        stdin=subprocess.PIPE)
    print("Encoding...")
    feed_file_to_handle_with_progress('test-out2.avi', p.stdin)
    p.wait()


def get_title(hwnd):
    return win32gui.GetWindowText(hwnd)


PID = None

def start_capture():
    global PID


    window = win32gui.GetForegroundWindow()
    title = get_title(window)

    cleanup()
    print("cleanup finished, calling subprocess")
    PID = subprocess.Popen('ffmpeg\\ffmpeg.exe -f gdigrab -i title="{}" '
                '-framerate 15 -vf "scale=\'iw/2\':-1" '
                '-c:v rawvideo -pix_fmt yuv420p '
                'test-out2.avi'.format(title),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        stdin=subprocess.PIPE)
    # out, err = PID.communicate()

    print("Capturing has begun. Press F9 again to stop!")

def stop_capture():
    global PID

    #PID.terminate()
    #win32api.TerminateProcess(int(PID._handle), -1)
    #os.system('TASKKILL /PID {}'.format(PID.pid))
    PID.stdin.write(b'q')
    PID.stdin.flush()
    PID.wait()
    PID = None

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
    hotpy.register(handle_f9, 'F9', ['Alt'])
    hotpy.register(lambda: False, 'F9', ['Ctrl'])  # exit

    print("A Series of Tubes, v0.1")
    print("A simple webm maker, by Quasar\n")

    print("Press Alt+F9 to start recording!")
    print("Press Ctrl+F9 to exit.\n\n")

    hotpy.listen()
def test():

    try:
        os.unlink('test-out.webm')
    except:
        pass

    name = '{}.webm'.format(namer.get_name())
    url = 'http://i.notabigtruck.com/i/tubes/{}'.format(name)

    print('Your url will be: {}'.format(url))

    encode_video()
    print('Uploading...')
    uploader.upload('test-out.webm', name)

def test2():

    start_capture()


if __name__ == '__main__':
    main()
    #test2()
