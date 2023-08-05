#coding=utf-8
import subprocess

def ping(host = "www.google.com"):
    """
    :param host:
    :return:
        avg round trip time (mss)
    """
    ping = subprocess.Popen(
        ["ping", "-c", "4", host],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    out, error = ping.communicate()
    # print(out)
    if out is None or out == "":
        return -1
    else:
        return str(out).split("/")[-3]


if __name__ == '__main__':
    print(ping("www.google.com"))