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
        curses.KEY_LEFT: "Left",
        curses.KEY_RIGHT: "Right"
    }

    stdscr.nodelay(True)
    stdscr.timeout(1)   

    stdscr.addstr(1, 0, "Use as setas do teclado para controlar. q para sair\n")
    stdscr.refresh()

    last_direction = None
    while True:
        key = stdscr.getch()
        if key in key_dict:
            direction = key_dict[key]
            stdscr.addstr(2, 0, f"{direction}")
            stdscr.refresh()

            step = 1
            if direction == "Left":
                direction = "Right"
                step = 5
            elif direction == "Right":
                direction = "Left"
                step = 5
        
            cam.ptz(f"Direction{direction}", step=step, preset=0)
            last_direction = direction
        
        elif key == ord('q'):
            break

        else:
            if last_direction is not None:
                cam.ptz(f"Direction{last_direction}", step=5, preset=-1)
            last_direction = None

        stdscr.move(2, 0)
        stdscr.clrtoeol()
        stdscr.refresh()

    # Just in case the program stops and the camera is still moving
    cam.ptz(f"DirectionDown", step=5, preset=-1)

if __name__ == "__main__":
    curses.wrapper(control_camera)

