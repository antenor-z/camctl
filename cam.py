import curses
from json import load
from dvrip import DVRIPCam
from time import sleep

def control_camera(stdscr):
    # Load camera configuration
    host_ip = '192.168.86.97'

    with open("config.json") as fp:
        auth = load(fp)
    cam = DVRIPCam(host_ip, user=auth["user"], password=auth["password"])
    if cam.login():
        stdscr.addstr(0, 0, f"{host_ip} OK\n")
    else:
        stdscr.addstr(0, 0, "FAIL\n")
        stdscr.refresh()
        sleep(2)
        return

    key_dict = {
        curses.KEY_UP: "Up",
        curses.KEY_DOWN: "Down",
        curses.KEY_LEFT: "Right",
        curses.KEY_RIGHT: "Left"
    }

    stdscr.nodelay(True)
    stdscr.timeout(100)

    stdscr.addstr(1, 0, "Use as setas para controlar a câmera. q para sair.\n")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in key_dict:
            direction = key_dict[key]
            stdscr.addstr(2, 0, f"{direction} pressionada  ")
            stdscr.refresh()

            cam.ptz(f"Direction{direction}", step=5, preset=0)
            sleep(0.3)
            cam.ptz(f"Direction{direction}", step=5, preset=-1)

        elif key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(control_camera)

