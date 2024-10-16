# Step Motor Control with CAN Bus Interface

This Python project provides a graphical user interface (GUI) for controlling a step motor via CAN bus communication. It's designed for precise motor control in various applications, such as robotics, automation, or any system requiring accurate positioning and velocity control.

## Features:

- Real-time motor control through a user-friendly GUI
- CAN bus communication for robust and reliable motor commands
- Motor enable/disable functionality
- Forward and backward velocity control
- Emergency stop function
- Position control with a slider interface (-10000 to 10000 range)
- Modular design for easy integration and expansion

## Technologies:

- Python 3.x
- Tkinter for GUI
- python-can library for CAN bus communication

## Usage:

This application allows users to:
1. Enable/disable the motor
2. Control motor velocity in both directions
3. Perform an emergency stop
4. Set precise motor positions using a slider

Ideal for developers and engineers working on projects that require fine-tuned step motor control with a simple, intuitive interface.

## Requirements:

- Python 3.x
- python-can
- A compatible CAN bus interface (configured for COM2 in this example)

## Getting Started:

Clone the repository, install the required dependencies, and run the `zdt_step_motor.py` script to launch the control interface.
