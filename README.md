# OpenBCI-controledPicoGoCar
https://drive.google.com/drive/folders/1NYkN86t4LOmo_f_R9RVOYEKSZ3UxlRYC
Overview
This project demonstrates a real-time human–machine interface where EMG (muscle) signals are used to control a mobile robot.

Signals are acquired using the OpenBCI Ganglion board, processed on a computer, and translated into commands that drive a PicoGo robot.

Control loop:

Human intent → EMG signal → Processing → Commands → Robot motion

The goal is reliable detection of human intent and its immediate execution, not autonomous navigation.

Architecture
User (muscle contraction)
        ↓
OpenBCI Ganglion
        ↓
Computer (BrainFlow + processing)
        ↓ USB
Raspberry Pi Pico (PicoGo)
        ↓
Motors → Movement

Signal processing is performed on a computer for stability and low latency, while the Pico handles motor control.

Hardware
OpenBCI Ganglion
EMG electrodes
PicoGo robot (Raspberry Pi Pico)
USB connection
Computer with Python
Software
BrainFlow (signal acquisition)
Python + NumPy (processing, RMS)
Serial communication (USB)
MicroPython (robot control)
How It Works

Calibration
The system measures baseline EMG activity and sets dynamic thresholds.

Detection
RMS of the signal is computed in real time.
Hysteresis is used to ensure stable activation.

Control Mapping

Action	Command
Left contraction	Left
Right contraction	Right
Chest contraction	Forward
Relaxed	Stop

Communication

F - forward
L - left
R - right
S - stop

Execution
The Pico reads commands and controls motors using PWM.

Key Decisions
USB over wireless — lower latency, higher reliability
RMS method — stable and computationally efficient
Hysteresis — prevents unstable switching
Notes
Slight drift during forward motion is expected (motor differences)
Turning may vary due to EMG signal variability
Safety

The system defaults to STOP when no valid signal is detected.

Future Improvements
Proportional speed control
Adaptive thresholds
Additional filtering
More gesture inputs
Wireless communication
Summary

The project demonstrates a closed-loop system where biological signals directly control a robot in real time.
