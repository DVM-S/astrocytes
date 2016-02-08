from pykinect2 import PyKinectV2
import pygame
import random


pygame.init()
bg = pygame.image.load('bgGame2.jpg')
scoreFont = pygame.font.Font(None, 40)

lateralShift = 896/2
chars = list('abcdefghijklmnopqrstuvwxyz')
vowels = list('aeiou')
charactersNormal = [x for x in chars]
charactersGood = charactersNormal + (1 * vowels)
charactersBad = list(set(charactersNormal) - set(vowels))
allParticles = []
livesLeft = 3
totalOrange = 0
font = pygame.font.Font(None, 40)


def generateParticles(number):
    global totalOrange

    newParticles = []
    for x in range(number):
        if totalOrange == 0:
            randomCharacter = random.sample(vowels, 1)[0]
        elif totalOrange <= 10:
            randomCharacter = random.sample(charactersGood, 1)[0]
        else:
            randomCharacter = random.sample(charactersBad, 1)[0]
        good = False
        if randomCharacter in vowels:
            good = True
            totalOrange += 1
        newParticle = Particle(randomCharacter, good)
        newParticles.append(newParticle)
    return newParticles


def collideParticles(basket1, basket2):
    global totalOrange
    global livesLeft

    scoreChange = 0
    for particle in allParticles:
        if particle.hidden:
            continue

        if particle.rect.y >= 768:
            particle.hidden = True
            if particle.good:
                livesLeft -= 1
                totalOrange -= 1

        if particle.rect.colliderect(basket1) or \
                particle.rect.colliderect(basket2):
            if particle.good:
                scoreChange += 2
                totalOrange -= 1
            else:
                scoreChange -= 1
            particle.hidden = True
    return (scoreChange, livesLeft)


def sizeCheck(joints, jointPoints, screen):
    joint0 = PyKinectV2.JointType_ShoulderLeft
    joint1 = PyKinectV2.JointType_ShoulderRight

    joint0State = joints[joint0].TrackingState
    joint1State = joints[joint1].TrackingState

    if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked):
        return

    if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
        return

    start = (jointPoints[joint0].x, jointPoints[joint0].y)
    end = (jointPoints[joint1].x, jointPoints[joint1].y)

    try:
        hipWidth = ((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5
        screenWidth = screen.get_width()
        return hipWidth / screenWidth > 0.1
    except:
        pass


def paintParticles(screen):
    for particle in allParticles:
        if not particle.hidden:
            particle.rect.y += 2
            screen.blit(particle.textSurface, particle.rect)


class Particle:

    def __init__(self, character, good):
        self.character = character
        self.font = pygame.font.Font(None, 100)
        self.good = good
        self.hidden = False
        self.textSurface = self.font.render('%s' % (character), 1, (0, 0, 0))
        self.rect = self.textSurface.get_rect()
        self.rect.x = random.randint(20+lateralShift, 1000+lateralShift)
        self.rect.y = -20
