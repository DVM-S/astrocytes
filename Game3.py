from pykinect2 import PyKinectV2

import random
import pygame
from math import atan2, degrees, pi


pygame.init()
pygame.display.set_mode((1024, 768), pygame.HWSURFACE | pygame.DOUBLEBUF, 32)
bg = pygame.image.load('bgGame3.jpg')

oldQuestions = []
questionFont = pygame.font.Font('IHATCS.TTF', 60)
operatorFont = pygame.font.Font('IHATCS.TTF', 60)
scoreFont = pygame.font.Font(None, 40)
solved = True
question = None
operator = None
curr = -1

angleFromOperator = {
    '+': [(0, 270), (270, 180)],
    'x': [(315, 225)],
    '-': [(None, 180), (0, None)],
    '/': [(None, 225)]
}


def checkMatch(operator, attemptAngles):
    if operator == '+':
        return (abs(270-attemptAngles[1]) <= 15 and abs(0-attemptAngles[0]) <= 15) or \
            (abs(180-attemptAngles[1]) <= 15 and abs(270-attemptAngles[0]) <= 15)

    elif operator == 'x':
        return (abs(225-attemptAngles[1]) <= 15 and abs(315-attemptAngles[0]) <= 15)

    elif operator == '-':
        return (abs(180-attemptAngles[1]) <= 15) or \
            (abs(0-attemptAngles[0]) <= 15)

    elif operator == '/':
        return (abs(225-attemptAngles[1]) <= 15)


def calculateAngles(joints, jointPoints, attemptAngles):
    angles = []
    for side in ['Right', 'Left']:
        joint0 = eval('PyKinectV2.JointType_Elbow%s' % (side))
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

questionList = [
    (2, 4, 6, '+'),
    (9, 3, 3, '/'),
    (2, 2, 0, '-'),
    (2, 4, 8, 'x'),
    (9, 5, 4, '-'),
    (2, 3, 5, '+'),
    (8, 4, 2, '/'),
    (1, 1, 0, '-'),
    (2, 4, 8, 'x'),
    (0, 1, 0, '/'),
]


def newQuestion():
    global curr
    print curr
    curr = (curr + 1) % len(questionList)
    return questionList[curr]
