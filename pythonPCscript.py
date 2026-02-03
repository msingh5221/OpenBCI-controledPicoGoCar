from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import numpy as np
import time
import serial

# ---------------- ROBOT (USB) ----------------
ROBOT_COM = "COM10"
BAUD = 115200

ser = serial.Serial(ROBOT_COM, BAUD, timeout=1)
time.sleep(2)

def send(cmd):
    ser.write((cmd + "\n").encode())

# ---------------- OPENBCI (Ganglion) ----------------
params = BrainFlowInputParams()
params.serial_port = "COM11"

board = BoardShim(BoardIds.GANGLION_BOARD.value, params)
board.prepare_session()
board.start_stream()

eeg_ch = BoardShim.get_eeg_channels(BoardIds.GANGLION_BOARD.value)

LEFT_CH    = eeg_ch[1]
RIGHT_CH   = eeg_ch[0]
FORWARD_CH = eeg_ch[2]   

WINDOW = 60
CALIBRATION_TIME = 10

def rms_strength(x):
    x = x - np.mean(x)
    return float(np.sqrt(np.mean(x * x)))

# ---------------- KALIBRACIJA ----------------
print("Kalibracija (miruj 10s)...")

left_list, right_list, forward_list = [], [], []
t0 = time.time()

while time.time() - t0 < CALIBRATION_TIME:
    data = board.get_current_board_data(WINDOW)
    if data.shape[1] > 0:
        left_list.append(rms_strength(data[LEFT_CH]))
        right_list.append(rms_strength(data[RIGHT_CH]))
        forward_list.append(rms_strength(data[FORWARD_CH]))
    time.sleep(0.1)

L_base, L_std = np.mean(left_list), np.std(left_list)
R_base, R_std = np.mean(right_list), np.std(right_list)
F_base, F_std = np.mean(forward_list), np.std(forward_list)

L_START, L_STOP = L_base + 5*L_std, L_base + 2*L_std
R_START, R_STOP = R_base + 5*R_std, R_base + 2*R_std
F_START, F_STOP = F_base + 5*F_std, F_base + 2*F_std

print("Kalibracija gotova")

# ---------------- STATE ----------------
left_on = False
right_on = False
forward_on = False  

last_cmd = "S"
send("S")

MIN_HOLD_SEC = 0.20
SWITCH_DEAD_SEC = 0.10

last_change_time = 0.0
last_switch_time = 0.0

print("Spremno")

try:
    while True:
        data = board.get_current_board_data(WINDOW)
        if data.shape[1] == 0:
            continue

        L = rms_strength(data[LEFT_CH])
        R = rms_strength(data[RIGHT_CH])
        F = rms_strength(data[FORWARD_CH])

        # LEFT
        if not left_on and L > L_START:
            left_on = True
        elif left_on and L < L_STOP:
            left_on = False

        # RIGHT
        if not right_on and R > R_START:
            right_on = True
        elif right_on and R < R_STOP:
            right_on = False

        # FORWARD
        if not forward_on and F > F_START:
            forward_on = True
        elif forward_on and F < F_STOP:
            forward_on = False

        if forward_on:
            cmd = "F"
        elif left_on and right_on:
            cmd = "F"
        elif left_on:
            cmd = "L"
        elif right_on:
            cmd = "R"
        else:
            cmd = "S"

        now = time.time()

        if cmd != last_cmd:
            if (now - last_change_time) < MIN_HOLD_SEC:
                cmd = last_cmd
            elif (now - last_switch_time) < SWITCH_DEAD_SEC:
                cmd = last_cmd

        if cmd != last_cmd:
            send(cmd)
            last_cmd = cmd
            last_change_time = now
            last_switch_time = now
            print("CMD:", cmd, "| L:", round(L,3), "R:", round(R,3), "F:", round(F,3))

        time.sleep(0.05)

except KeyboardInterrupt:
    send("S")

finally:
    board.stop_stream()
    board.release_session()
    ser.close()
