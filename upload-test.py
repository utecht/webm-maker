import paramiko
import progressbar


def progress(current, total):
    if progress.bar is None:
        widgets = [progressbar.Percentage(),
                   progressbar.Bar(),
                   progressbar.ETA(),
                   progressbar.FileTransferSpeed()]
        progress.bar = progressbar.ProgressBar(widgets=widgets, maxval=total)
        progress.bar.start()
    if current == total:
        progress.bar.finish()
    else:
        progress.bar.update(current)
progress.bar = None


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect("quasarj.com", username="truckload", password="4hg0sn33k")
sftp = client.open_sftp()

print("Connected, beginning upload...")
sftp.put('nerds.webm', 'tubes/nerds.webm', progress)

print("Complete, exiting")
client.close()
