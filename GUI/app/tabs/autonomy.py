from __future__ import annotations
from pynput import keyboard

import functools
import json
from typing import List

from bell.avr.mqtt.payloads import (
    AvrAutonomousBuildingDropPayload,
    AvrAutonomousEnablePayload,
    AvrPcmSetServoAbsPayload,
    #AvrPcmStepperMovePayload,
)
from PySide6 import QtCore, QtWidgets

from ..lib.color import wrap_text
from .base import BaseTabWidget
import time

halfstep_seq_frw = [
         [1,0,0,0],
         [1,1,0,0],
         [0,1,0,0],
         [0,1,1,0],
         [0,0,1,0],
         [0,0,1,1],
         [0,0,0,1],
         [1,0,0,1]
    ]
halfstep_seq_bck = [
        [1,0,0,1],
        [0,0,0,1],
        [0,0,1,1],
        [0,0,1,0],
        [0,1,1,0],
        [0,1,0,0],
        [1,1,0,0],
        [1,0,0,0]
     ]


class AutonomyWidget(BaseTabWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.setWindowTitle("Autonomy")


    def build(self) -> None:
        """
        Build the GUI layout
        """
        layout = QtWidgets.QGridLayout(self)
        self.setLayout(layout)

        # ==========================
        # Autonomous mode ha nope I murdered your code and turned it's ashes into a beautiful new creation that will destroy you on the feild of battle


        LinearActuator_groupbox = QtWidgets.QGroupBox("LinearActuator")
        LinearActuator_layout = QtWidgets.QVBoxLayout()
        LinearActuator_groupbox.setLayout(LinearActuator_layout)

        Up_button = QtWidgets.QPushButton("Up")
        LinearActuator_layout.addWidget(Up_button)
        Up_button.clicked.connect(lambda: self.Up())

        Down_button = QtWidgets.QPushButton("Down")
        LinearActuator_layout.addWidget(Down_button)
        Down_button.clicked.connect(lambda: self.Down())

        Off_button = QtWidgets.QPushButton("Off")
        LinearActuator_layout.addWidget(Off_button)
        Off_button.clicked.connect(lambda: self.Off())

        layout.addWidget(LinearActuator_groupbox)

        """
        Sucker_groupbox = QtWidgets.QGroupBox("Sucker")
        Sucker_layout = QtWidgets.QVBoxLayout()
        Sucker_groupbox.setLayout(Sucker_layout)

        Suck_button = QtWidgets.QPushButton("Suck")
        Sucker_layout.addWidget(Suck_button)

        Suck_button.clicked.connect(lambda: self.Suck())

        Off_button = QtWidgets.QPushButton("Off")
        Sucker_layout.addWidget(Off_button)

        Off_button.clicked.connect(lambda: self.Off())

        Spit_button = QtWidgets.QPushButton("Spit")
        Sucker_layout.addWidget(Spit_button)

        Spit_button.clicked.connect(lambda: self.Spit())

        arm_button = QtWidgets.QPushButton("arm")
        Sucker_layout.addWidget(arm_button)

        arm_button.clicked.connect(lambda: self.arm())

        layout.addWidget(Sucker_groupbox)
        """

    """
    def on_press(self, key):  # sourcery skip
        try:
            k = key.char  # single-char keys
            if k == "q":
                self.set_servo_pos(1, 1000)
            elif k == "w":
                self.set_servo_pos(1, 1125)
            elif k == "e":
                self.set_servo_pos(1, 1250)
            elif k == "r":
                self.set_servo_pos(1, 1375)
            elif k == "o":
                self.set_servo_pos(2, 2000)
            elif k == "p":
                self.set_servo_pos(2, 1000)
        except Exception:
            pass #need something here for a try except statemet

   """

    def Up (self) -> None:
        data = {"command":"U"}
        json_data = json.dumps(data, indent=4)
        self.send_message(
            "avr/pcm/stepper/linearactuator",
            data
            #AvrPcmStepperMovePayload(steps=0,direction="U")
        )

    def Down (self) -> None:
        data = {"command":"D"}
        self.send_message(
            "avr/pcm/stepper/linearactuator",
            data
            #AvrPcmStepperMovePayload(steps=0,direction="U")
        )

    def Off (self) -> None:
        data = {"command":"O"}
        self.send_message(
            "avr/pcm/stepper/linearactuator",
            data
            #AvrPcmStepperMovePayload(steps=0,direction="U")
        )

    def Suck (self) -> None:
        self.set_servo_pos(1,1000)
        """
        self.send_message(
            "avr/pcm/stepper/move",
            AvrPcmStepperMovePayload(steps=0,direction="U")
        )
        print ("sending mesage")
        """

    def Spit (self) -> None:
        self.set_servo_pos(1,2000)
        """
        self.send_message(
            "avr/pcm/stepper/move",
            AvrPcmStepperMovePayload(steps=0,direction="D")
        )
        """
    # def Off (self) -> None:
        # self.set_servo_pos(3,0)
        """
        self.send_message(
            "avr/pcm/stepper/move",
            AvrPcmStepperMovePayload(steps=0,direction="O")
        )
        print ("stopping sending mesage")
        """

    def set_servo_pos(self, number: int, position: int) -> None:
        """
        Set a servo state
        """
        self.send_message(
            "avr/pcm/set_servo_abs",
            AvrPcmSetServoAbsPayload(servo=number, absolute=position),
        )

    def arm (self) -> None:
        self.set_servo_pos(3,2000)





"""
servo contol example
def on_press(self, key):  # sourcery skip
        try:
            #dont judge the if else list because its dogshit code
            #why the fuck did I not make this a switch MAKE IT A SWITCH DUMBASS
            k = key.char  # single-char keys
            if k == "q":  #seal
                self.set_servo_pos(1, 2000)
            elif k == "w": #open
                self.set_servo_pos(1, 400) #400????????
            elif k == "y": #swing arm
                self.set_servo_pos(4, 800)
            elif k == "u": #swing arm halfway to mid
                self.set_servo_pos(4, 1000)
            elif k == "i": #swing arm to middle
                self.set_servo_pos(4, 1400)
            elif k == "o": #swing arm halfway to end
                self.set_servo_pos(4, 1600)
            elif k == "p": #swing arm to end
                self.set_servo_pos(4, 1800)
            #fan pwm outputs
            elif k == "0":
                self.set_servo_pos(0, 1000)
            elif k == "1":
                self.set_servo_pos(0, 1200)
            elif k == "2":
                self.set_servo_pos(0, 1400)
            elif k == "3":
                self.set_servo_pos(0, 1600)
            elif k == "4":
                self.set_servo_pos(0, 1800)
            elif k == "5":
                self.set_servo_pos(0, 2000)
        except Exception:
            pass #need something here for a try except statemet
            """

