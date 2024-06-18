import curses
from json import load
from dvrip import DVRIPCam
from time import sleep

# Load camera configuration
host_ip = '192.168.86.97'

with open("config.json") as fp:
        auth = load(fp)
        cam = DVRIPCam(host_ip, user=auth["user"], password=auth["password"])
        if cam.login():
                print(f"{host_ip} OK")
        else:
                print("FAIL")
