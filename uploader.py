import paramiko
import progressbar

import settings

def make_progress_callback():
    bar = None

    def progress(current, total):
        nonlocal bar
        if bar is None:
            widgets = [progressbar.Percentage(), ' ',
                       progressbar.Bar(), ' ',
                       progressbar.ETA(), ' ',
                       progressbar.FileTransferSpeed()]
            bar = progressbar.ProgressBar(widgets=widgets, maxval=total)
            bar.start()
        if current == total:
            bar.finish()
        else:
            bar.update(current)

    return progress


def upload(source_filename, dest_filename):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(settings.hostname,
                   username=settings.username,
                   password=settings.password)
    sftp = client.open_sftp()

    # print("Connected, beginning upload...")
    sftp.put(source_filename, 'tubes/' + dest_filename, make_progress_callback())

    # print("Complete, exiting")
    client.close()


if __name__ == '__main__':
    import sys
    upload(sys.argv[1], sys.argv[1])
