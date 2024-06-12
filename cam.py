from json import load
from dvrip import DVRIPCam
from time import sleep

host_ip = '192.168.86.97'

with open("config.json") as fp:
    auth = load(fp)
cam = DVRIPCam(host_ip, user=auth["user"], password=auth["password"])
if cam.login():
	print(host_ip, "OK")
else:
	print("FAIL")

key_dict = {
    "u": "Up",
    "d": "Down",
    "r": "Left",
    "l": "Right"
}
while True:
        a = input()
        dir, duration = a[0], a[1:]
        if dir in key_dict.keys():
                dir = key_dict[dir]
                if dir in ["Up", "Down"]:
                    duration = int(duration) / 3
                cam.ptz(f"Direction{dir}", step=5, preset=0)
                sleep(int(duration) / 10)
                cam.ptz(f"Direction{dir}", step=5, preset=-1)

