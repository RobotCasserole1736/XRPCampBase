#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

#
# Example that shows how to connect to a XRP from RobotPy
#
# Requirements
# ------------
#
# You must have the robotpy-halsim-ws package installed. This is best done via:
#
#    # Windows
#    py -3 -m pip install robotpy[commands2,sim]
#
#    # Linux/macOS
#    pip3 install robotpy[commands2,sim]
#
# Run the program
# ---------------
#
# To run the program you will need to explicitly use the ws-client option:
#
#    # Windows
#    py -3 robotpy sim --ws-client
#
#    # Linux/macOS
#    python robotpy sim --ws-client
#
# By default the WPILib simulation GUI will be displayed. To disable the display
# you can add the --nogui option
#

import os

import wpilib
from wpimath.geometry import Rotation2d

from xrp import XRPGyro
from xrp import XRPMotor


# Configure XRP communication
os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"


class MyRobot(wpilib.TimedRobot):

    def robotInit(self) -> None:
        self.controller = wpilib.XboxController(0)
        self.gyro = XRPGyro()
        self.leftMotor = XRPMotor(0)
        self.rightMotor = XRPMotor(1)
        self.rightMotor.setInverted(True)
        self.desAngle = 0.0

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        pass

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""
        pass


    def teleopInit(self) -> None:
        """This function is called once each time the robot enters Teleop mode."""
        self.gyro.reset()
        self.desAngle = Rotation2d(0.0)

    def teleopPeriodic(self) -> None:
        fwdRevCmd = -1.0 * self.controller.getLeftY()
        rotCmd = -1.0 * self.controller.getLeftX() # positive rotCmd is rotate to the left
        gyroAngle = self.gyro.getRotation2d()

        if(rotCmd != 0.0):
            # reset desired angel to current
            self.desAngle = gyroAngle
        else:
            # Apply gyro comp
            rotCmd = (self.desAngle.degrees() - gyroAngle.degrees()) * 0.05


        leftMotorSpeed = fwdRevCmd - rotCmd
        rightMotorSpeed = fwdRevCmd + rotCmd
        self.leftMotor.set(leftMotorSpeed)
        self.rightMotor.set(rightMotorSpeed)
        wpilib.SmartDashboard.putNumber("Gyro Angle (deg)", gyroAngle.degrees())
        wpilib.SmartDashboard.putNumber("Target Angle (deg)", self.desAngle.degrees())
        wpilib.SmartDashboard.putNumber("Rotation Command", rotCmd)
        wpilib.SmartDashboard.putNumber("FwdRev Command", fwdRevCmd)

