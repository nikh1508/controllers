from evdev import InputDevice, categorize, ecodes
import threading

gamepad = InputDevice('/dev/input/event18')

print(gamepad)

## EVENT NAMES ##
event_name = ["L1", "L2", "R1" ,"R2" ,"LT", "RT", "UP", "DN", "Y", "B", "A", "X", "LX", "LY", "RX", "RY", "LB", "RB", "BK", "ST", "MD"]

## EVENT CODES ##
event_index = {
    310 : 0,
    2 : 1,
    311 : 2,
    5 : 3,
    16 : 4,
    17 : 6,
    308 : 8,
    305 : 9,
    304 : 10,
    307 : 11,
    0 : 12,
    1 : 13,
    3 : 14,
    4 : 15,
    317 : 16,
    318 : 17,
    314 : 18,
    315 : 19,
    316 : 20
}

event_val = [0] * 21
event_val[12] = 128
event_val[13] = -129
event_val[14] = 128
event_val[15] = -129

def read_gamepad():
    global event_val
    for event in gamepad.read_loop():
        if event.code == 0 and event.value == 0:
            continue
        elif (event.code == 16 or event.code == 17):
            if(event.code ==16):
                index = 4
            else:
                index = 6
            if (event.value == -1):
                event_val[index] = 1
                event_val[index+1] = 0
            elif (event.value == 0):
                event_val[index] = 0
                event_val[index+1] = 0
            elif (event.value == 1):
                event_val[index] = 0
                event_val[index+1] = 1
        else:
            event_val[event_index[event.code]] = event.value

def print_data():
    while(True):
        for i in range(21):
            print("%s:%d   " %(event_name[i], event_val[i]), end='')
        print()

Thread1 = threading.Thread(target=read_gamepad)
Thread2 = threading.Thread(target=print_data)

Thread1.start()
Thread2.start()