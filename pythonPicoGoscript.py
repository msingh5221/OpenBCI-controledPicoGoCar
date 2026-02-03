from machine import Pin, PWM
import sys
import time

# =========================
# MOTOR KLASA
# =========================
class PicoGo(object):
    def __init__(self):
        self.PWMA = PWM(Pin(16))
        self.PWMA.freq(1000)
        self.AIN2 = Pin(17, Pin.OUT)
        self.AIN1 = Pin(18, Pin.OUT)

        self.BIN1 = Pin(19, Pin.OUT)
        self.BIN2 = Pin(20, Pin.OUT)
        self.PWMB = PWM(Pin(21))
        self.PWMB.freq(1000)

        self.stop()

    def forward(self, speed):
        if 0 <= speed <= 100:
            duty = int(speed * 0xFFFF / 100)
            self.PWMA.duty_u16(duty)
            self.PWMB.duty_u16(duty)
            self.AIN2.value(1)
            self.AIN1.value(0)
            self.BIN2.value(1)
            self.BIN1.value(0)

    def left(self, speed):
        if 0 <= speed <= 100:
            duty = int(speed * 0xFFFF / 100)
            self.PWMA.duty_u16(duty)
            self.PWMB.duty_u16(duty)
            self.AIN2.value(0)
            self.AIN1.value(1)
            self.BIN2.value(1)
            self.BIN1.value(0)

    def right(self, speed):
        if 0 <= speed <= 100:
            duty = int(speed * 0xFFFF / 100)
            self.PWMA.duty_u16(duty)
            self.PWMB.duty_u16(duty)
            self.AIN2.value(1)
            self.AIN1.value(0)
            self.BIN2.value(0)
            self.BIN1.value(1)

    def stop(self):
        self.PWMA.duty_u16(0)
        self.PWMB.duty_u16(0)
        self.AIN2.value(0)
        self.AIN1.value(0)
        self.BIN2.value(0)
        self.BIN1.value(0)

# =========================
# MAIN PROGRAM
# =========================
robot = PicoGo()

SPEED_FWD = 60
SPEED_TURN = 45

print("===================================")
print(" PicoGo READY (EMG USB CONTROL)")
print(" Commands: F L R S")
print("===================================")

buffer = ""

while True:
    ch = sys.stdin.read(1)

    if ch:
        if ch == "\n":
            cmd = buffer.strip().upper()
            buffer = ""

            if cmd == "F":
                robot.forward(SPEED_FWD)
                print("FORWARD")

            elif cmd == "L":
                robot.left(SPEED_TURN)
                print("LEFT")

            elif cmd == "R":
                robot.right(SPEED_TURN)
                print("RIGHT")

            elif cmd == "S":
                robot.stop()
                print("STOP")

            else:
                print("UNKNOWN CMD:", cmd)

        else:
            buffer += ch

    time.sleep(0.01)
