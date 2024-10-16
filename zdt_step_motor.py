import can
import time
from tkinter import *
from tkinter import ttk

# CAN bus setup
bus = can.interface.Bus(bustype='slcan', channel='COM2', bitrate=500000)

# Motor address
MOTOR_ADDR = 1

def send_can_command(cmd, cmd_len):
    i = 0
    j = cmd_len - 2  # Excluding ID address and function code
    packNum = 0

    while i < j:
        k = j - i  # Remaining data count

        # Prepare the message
        arbitration_id = (cmd[0] << 8) | packNum
        data = [cmd[1]]  # Function code

        if k < 8:
            data.extend(cmd[2+i:2+i+k])
            dlc = k + 1
        else:
            data.extend(cmd[2+i:2+i+7])
            dlc = 8

        # Create and send the CAN message
        msg = can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=True,
            dlc=dlc
        )
        bus.send(msg)

        i += len(data) - 1  # -1 because we already included the function code
        packNum += 1

def motor_enable(state):
    cmd = [MOTOR_ADDR, 0xF3, 0xAB, state, 0, 0x6B]
    send_can_command(cmd, 6)

def motor_velocity_control(direction, velocity, acceleration):
    cmd = [MOTOR_ADDR, 0xF6, direction, 
           (velocity >> 8) & 0xFF, velocity & 0xFF, 
           acceleration, 0, 0x6B]
    send_can_command(cmd, 8)

def motor_stop():
    cmd = [MOTOR_ADDR, 0xFE, 0x98, 0, 0x6B]
    send_can_command(cmd, 5)

def motor_position_control(position):
    direction = 1 if position >= 0 else 0
    abs_position = abs(position)
    cmd = [MOTOR_ADDR, 0xFD, direction, 
           500 >> 8, 500 & 0xFF,  # Velocity: 1000 RPM
           0,  # Acceleration: 10
           (abs_position >> 24) & 0xFF, (abs_position >> 16) & 0xFF,
           (abs_position >> 8) & 0xFF, abs_position & 0xFF,
           1, 0, 0x6B]
    send_can_command(cmd, 13)

def on_forward():
    motor_velocity_control(1, 400, 0)  # CCW direction, 1000 RPM, acceleration 10

def on_backward():
    motor_velocity_control(0, 400, 0)  # CW direction, 1000 RPM, acceleration 10

def on_stop():
    motor_stop()

def on_enable():
    motor_enable(1)
    enable_button.config(text="Disable", command=on_disable)

def on_disable():
    motor_enable(0)
    enable_button.config(text="Enable", command=on_enable)

def on_position_change(value):
    position = int(float(value))
    motor_position_control(position)

# GUI setup
root = Tk()
root.title("Step Motor Control")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(N, W, E, S))

enable_button = ttk.Button(frame, text="Enable", command=on_enable)
enable_button.grid(column=0, row=0, padx=5, pady=5)

ttk.Button(frame, text="Forward", command=on_forward).grid(column=1, row=0, padx=5, pady=5)
ttk.Button(frame, text="Backward", command=on_backward).grid(column=2, row=0, padx=5, pady=5)
ttk.Button(frame, text="Stop", command=on_stop).grid(column=3, row=0, padx=5, pady=5)

# Position control slider
ttk.Label(frame, text="Position Control:").grid(column=0, row=1, padx=5, pady=5)
position_slider = ttk.Scale(frame, from_=-10000, to=10000, orient=HORIZONTAL, length=300, command=on_position_change)
position_slider.grid(column=1, row=1, columnspan=3, padx=5, pady=5)

root.mainloop()
