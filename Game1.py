from pykinect2 import PyKinectV2

import random
import pygame
from math import atan2, degrees, pi


pygame.init()
pygame.display.set_mode((1024, 768), pygame.HWSURFACE | pygame.DOUBLEBUF, 32)
bg = pygame.image.load('bgGame1.jpg')
hourHand = pygame.image.load('hshort2.png').convert_alpha()
minuteHand = pygame.image.load('hand.png').convert_alpha()

leftNeedle = hourHand
rightNeedle = minuteHand

hours = [(i+1) for i in range(12)]
hours = hours[:9]
minutes = [i for i in range(0, 60, 15)]
oldTimes = []

timeFont = pygame.font.Font('DS-DIGIB.TTF', 40)
scoreFont = pygame.font.Font(None, 40)
solved = True
time = None


def checkMatch(correctAngles, attemptAngles):
    (correctAngleRight, correctAngleLeft) = correctAngles
    (attemptAnglesRight, attemptAnglesLeft) = attemptAngles
    return abs(correctAngleLeft-attemptAnglesLeft) <= 15 and abs(correctAngleRight-attemptAnglesRight) <= 15


def calculateAngles(joints, jointPoints, attemptAngles):
    angles = []
    for side in ['Right', 'Left']:
        joint0 = eval('PyKinectV2.JointType_Shoulder%s' % (side))
        joint1 = eval('PyKinectV2.JointType_Hand%s' % (side))

        joint0State = joints[joint0].TrackingState
        joint1State = joints[joint1].TrackingState

        if (joint0State == PyKinectV2.TrackingState_NotTracked) or \
                (joint1State == PyKinectV2.TrackingState_NotTracked):
            return attemptAngles

        if (joint0State == PyKinectV2.TrackingState_Inferred) and \
                (joint1State == PyKinectV2.TrackingState_Inferred):
            return attemptAngles

        (x2, y2) = jointPoints[joint0].x, jointPoints[joint0].y
        (x1, y1) = jointPoints[joint1].x, jointPoints[joint1].y
        dx = x2 - x1
        dy = y2 - y1
        rads = atan2(-dy, dx)
        rads %= 2*pi
        degs = degrees(rads)
        angles.append(degs)
    return angles


def angleFromTime(time):
    (hour, minute) = time
    hourRight = [1, 2, 3, 4, 5, 6]
    hourLeft = [7, 8, 9, 10, 11, 12]
    rightAngle = leftAngle = 'unassigned'

    if hour in hourRight:
        rightAngle = abs(hour * 30 - 270)
    else:
        leftAngle = abs(hour * 30 - 270)
    minutesAngle = {
        0: 270,
        15: 180,
        30: 90,
        45: 0,
        60: 270
    }

    if rightAngle == 'unassigned':
        rightAngle = minutesAngle[minute]
    else:
        leftAngle = minutesAngle[minute]

    return (rightAngle, leftAngle)


def newTime():
    hour = random.sample(hours, 1)[0]
    minute = random.sample(minutes, 1)[0]
    time = (hour, minute)
    return time
