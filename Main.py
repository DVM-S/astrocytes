from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
import sys

import random
import Game1
import Game2
import Game3

CHANGE_MUSIC = 29
SKELETON_COLORS = (255, 0, 0)


class Main(object):

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Game')

        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        # self._kinect.max_body_count = 6
        self._bodies = None

        self.clock = pygame.time.Clock()
        pygame.time.set_timer(30, 1000)
        self.screen = pygame.display.set_mode((1024, 768), pygame.HWSURFACE | pygame.DOUBLEBUF, 32)
        self.canvas = pygame.Surface((1920, 1080), 0, 32)
        self.bg = None

        self.bgmPlaying = False
        self.chosen = 'Menu'
        self.score = 0
        attemptAngles = (0, 0)

    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1, mode='thin'):
        joint0State = joints[joint0].TrackingState
        joint1State = joints[joint1].TrackingState

        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked):
            return

        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            width = 30
            if mode == 'thin':
                pygame.draw.line(self.canvas, color, start, end, width)
            elif mode == 'thick':
                start = [int(xy) for xy in start]
                end = [int(xy) for xy in end]
                pygame.draw.circle(self.canvas, color, start, (width/2))
                pygame.draw.circle(self.canvas, color, end, (width/2))
        except:
            pass

    def draw_body(self, joints, jointPoints, color):
        # thin
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft, 'thin')

        # Right Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight, 'thin')

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft, 'thin')

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight, 'thin')

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft, 'thin')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft, 'thin')

        # thick drawings
        # Right Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight, 'thick')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight, 'thick')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight, 'thick')

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft, 'thick')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft, 'thick')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft, 'thick')

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight, 'thick')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight, 'thick')

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft, 'thick')
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft, 'thick')

        # polygon drawings
        # Torso
        pygame.draw.polygon(self.canvas, color, [
            (jointPoints[PyKinectV2.JointType_SpineShoulder].x, jointPoints[PyKinectV2.JointType_SpineShoulder].y),
            (jointPoints[PyKinectV2.JointType_ShoulderLeft].x, jointPoints[PyKinectV2.JointType_ShoulderLeft].y),
            (jointPoints[PyKinectV2.JointType_HipLeft].x-20, jointPoints[PyKinectV2.JointType_HipLeft].y),
            (jointPoints[PyKinectV2.JointType_HipRight].x+20, jointPoints[PyKinectV2.JointType_HipRight].y),
            (jointPoints[PyKinectV2.JointType_ShoulderRight].x, jointPoints[PyKinectV2.JointType_ShoulderRight].y),
        ])
        # Head
        pygame.draw.circle(self.canvas, color, [
            int(jointPoints[PyKinectV2.JointType_Head].x), int(jointPoints[PyKinectV2.JointType_Head].y+10)
        ], 60)

    def music_player(self, chosen):
        songs_dict = {
            'Game1': 'bgmGame1.mp3',
            'Game2': 'bgmGame2.mp3',
            'Menu': 'bgmMenu.mp3',
        }
        pygame.mixer.music.load(songs_dict[chosen])
        pygame.mixer.music.play(-1)

    def run(self):
        angle = -10
        # pygame.mixer.music.load('bgmMenu.mp3')
        # pygame.mixer.music.play(-1)
        cm_event = pygame.event.Event(CHANGE_MUSIC)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == CHANGE_MUSIC:
                    self.music_player(self.chosen)
                elif event.type == 30:
                    if self.chosen == 'Game2':
                        newParticles = self.game.generateParticles(1)
                        self.game.allParticles.extend(newParticles)

            if self.chosen == 'Menu':
                bgMenu = pygame.image.load('bgMenu.png').convert()

                game1 = pygame.image.load('game1.1.png').convert_alpha()
                game2 = pygame.image.load('game2.1.png').convert_alpha()
                game3 = pygame.image.load('game3.1.png').convert_alpha()
                quit = pygame.image.load('quit.1.png').convert_alpha()

                game1H = pygame.image.load('game1.2.png').convert_alpha()
                game2H = pygame.image.load('game2.2.png').convert_alpha()
                game3H = pygame.image.load('game3.2.png').convert_alpha()
                quitH = pygame.image.load('quit.2.png').convert_alpha()

                mouse = pygame.mouse.get_pos()
                self.screen.blit(bgMenu, (0, 0))
                self.screen.blit(game1, (350, 350-50))
                self.screen.blit(game2, (350, 420-50))
                self.screen.blit(game3, (350, 490-50))
                self.screen.blit(quit, (350, 560-50))

                if 350+375 > mouse[0] > 350 and 300+57 > mouse[1] > 300:
                    self.screen.blit(game1H, (350, 350-50))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.chosen = 'Game1'
                        self.game = Game1

                if 350+375 > mouse[0] > 350 and 420-50+57 > mouse[1] > 420-50:
                    self.screen.blit(game2H, (350, 420-50))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.chosen = 'Game2'
                        self.game = Game2

                if 350+375 > mouse[0] > 350 and 490-50+57 > mouse[1] > 490-50:
                    self.screen.blit(game3H, (350, 490-50))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.chosen = 'Game3'
                        self.game = Game3

                if 350+375 > mouse[0] > 350 and 560-50+57 > mouse[1] > 560-50:
                    self.screen.blit(quitH, (350, 560-50))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        sys.exit(0)

            elif self.chosen == 'Game1':
                attemptAngles = (0, 0)
                self.bg = self.game.bg
                self.screen.blit(self.bg, (0, 0))
                # self.bgm = pygame.mixer.music.load('bgmTellTime.mp3')
                if self.game.solved:
                    # pygame.mixer.music.load('solved.mp3')
                    # pygame.mixer.music.play(0)
                    self.game.time = self.game.newTime()
                    if self.game.time[0] not in [1, 2, 3, 4, 5, 6]:
                        self.game.leftNeedle, self.game.rightNeedle = self.game.minuteHand, self.game.hourHand
                    else:
                        self.game.rightNeedle, self.game.leftNeedle = self.game.minuteHand, self.game.hourHand
                    self.score += 5
                    self.game.solved = False

                if self._kinect.has_new_body_frame():
                    self._bodies = self._kinect.get_last_body_frame()

                if self._bodies is not None:
                    for i in range(self._kinect.max_body_count):
                        body = self._bodies.bodies[i]
                        if not body.is_tracked:
                            continue

                        joints = body.joints
                        jointPoints = self._kinect.body_joints_to_color_space(joints)
                        attemptAngles = self.game.calculateAngles(joints, jointPoints, attemptAngles)
                        correctAngles = self.game.angleFromTime(self.game.time)
                        # hourHandRotated = pygame.transform.rotate(self.game.hourHand, attemptAngles[0])
                        # self.screen.blit(hourHandRotated, (504 - hourHandRotated.get_rect().width/2, 371 - hourHandRotated.get_rect().height/2))

                        # minuteHandRotated = pygame.transform.rotate(self.game.minuteHand, attemptAngles[1])
                        # self.screen.blit(minuteHandRotated, (504 - minuteHandRotated.get_rect().width/2, 371 - minuteHandRotated.get_rect().height/2))

                        leftNeedleRotated = pygame.transform.rotate(self.game.leftNeedle, attemptAngles[0])
                        self.screen.blit(leftNeedleRotated, (504 - leftNeedleRotated.get_rect().width/2, 371 - leftNeedleRotated.get_rect().height/2))

                        rightNeedleRotated = pygame.transform.rotate(self.game.rightNeedle, attemptAngles[1])
                        self.screen.blit(rightNeedleRotated, (504 - rightNeedleRotated.get_rect().width/2, 371 - rightNeedleRotated.get_rect().height/2))

                        self.game.solved = self.game.checkMatch(correctAngles, attemptAngles)

                timeSurface = self.game.timeFont.render(
                    '%02d:%02d' % (self.game.time), 1, (25, 25, 25))
                timePos = timeSurface.get_rect()
                timePos.centerx = self.screen.get_rect().centerx
                timePos.centery = 90
                self.screen.blit(timeSurface, timePos)

                scoreSurface = self.game.scoreFont.render(
                    '%02d' % self.score, 1, (25, 25, 25))
                self.screen.blit(scoreSurface, (140, 150))

            elif self.chosen == 'Game2':
                lateralShift = self.game.lateralShift
                self.bg = self.game.bg
                self.canvas.blit(self.bg, (0+lateralShift, 0))

                BLUE = (0, 125, 255)

                if self._kinect.has_new_body_frame():
                    self._bodies = self._kinect.get_last_body_frame()

                if self._bodies is not None:
                    for i in range(self._kinect.max_body_count):
                        body = self._bodies.bodies[i]
                        if not body.is_tracked:
                            continue

                        joints = body.joints
                        jointPoints = self._kinect.body_joints_to_color_space(joints)
                        self.draw_body(joints, jointPoints, SKELETON_COLORS)
                        tooLarge = self.game.sizeCheck(joints, jointPoints, self.screen)
                        if tooLarge:
                            errorFont = pygame.font.SysFont(None, 40)
                            errorSurface = errorFont.render('TOO CLOSE!', 1, (255, 0, 255))
                            self.canvas.blit(errorSurface, (100 + lateralShift, 0))

                        basket1 = pygame.Rect(jointPoints[PyKinectV2.JointType_HandRight].x - 25, jointPoints[PyKinectV2.JointType_HandRight].y - 25, 50, 50)
                        basket2 = pygame.Rect(jointPoints[PyKinectV2.JointType_HandLeft].x - 25, jointPoints[PyKinectV2.JointType_HandLeft].y - 25, 50, 50)

                        pygame.draw.rect(self.canvas, BLUE, basket1)
                        pygame.draw.rect(self.canvas, BLUE, basket2)

                        (scoreChange, lives) = self.game.collideParticles(basket1, basket2)
                        self.score += scoreChange
                        if lives == 0:
                            score = 0
                            print 'NO LIVES LEFT'

                self.game.paintParticles(self.canvas)
                scoreSurface = self.game.scoreFont.render(
                    '%02d' % self.score, 1, (225, 225, 225))
                self.canvas.blit(scoreSurface, (750+lateralShift, 60))
                self.screen.blit(self.canvas, (-lateralShift, 0))

            elif self.chosen == 'Game3':
                attemptAngles = (0, 0)
                self.bg = self.game.bg
                self.screen.blit(self.bg, (0, 0))

                if self.game.solved:
                    op = self.game.operatorFont.render('%s' % (self.game.operator), 1, (255, 255, 255))
                    self.screen.blit(op, (430, 340))

                    self.game.question = self.game.newQuestion()
                    self.game.operator = self.game.question[-1]
                    self.score += 5
                    self.game.solved = False

                A = self.game.questionFont.render('%d' % (self.game.question[0]), 1, (255, 255, 255))
                B = self.game.questionFont.render('%d' % (self.game.question[1]), 1, (255, 255, 255))
                C = self.game.questionFont.render('%d' % (self.game.question[2]), 1, (255, 255, 255))
                eq = self.game.questionFont.render('=', 1, (255, 255, 255))

                self.screen.blit(A, (340, 340))
                self.screen.blit(B, (500, 340))
                self.screen.blit(C, (650, 340))
                self.screen.blit(eq, (580, 340))


                if self._kinect.has_new_body_frame():
                    self._bodies = self._kinect.get_last_body_frame()

                if self._bodies is not None:
                    for i in range(self._kinect.max_body_count):
                        body = self._bodies.bodies[i]
                        if not body.is_tracked:
                            continue

                        joints = body.joints
                        jointPoints = self._kinect.body_joints_to_color_space(joints)
                        attemptAngles = self.game.calculateAngles(joints, jointPoints, attemptAngles)
                        self.game.solved = self.game.checkMatch(self.game.operator, attemptAngles)

                scoreSurface = self.game.scoreFont.render(
                    '%02d' % self.score, 1, (255, 255, 255))
                self.screen.blit(scoreSurface, (900, 115))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    game = Main()
    game.run()
