import pygame
import os

SMALLBUTTON_SIZE = (40,20)
SMALLBUTTON_NAME = 'smallbutton.jpg'

class Button(object):
    #initialize
    def __init__(self, surface, Postion, ImageName = SMALLBUTTON_NAME,
     ImageSize = SMALLBUTTON_SIZE, PassingByImageName = None, PassingByImage = None):

        self.Surface = surface
        self.WIDTH = ImageSize[0]
        self.HEIGHT = ImageSize[1]
        self.X = Postion[0]
        self.Y = Postion[1]

        # Passingby image provides two ways
        self.PBImage = PassingByImage
        self.__initPBImage(PassingByImageName)
        self.Image = self.__initImage(ImageName, ImageSize)


    def __initImage(self, ImageName, ImageSize):
        if ImageName is None:
            return None
        pathname = os.path.join('image', 'button' ,ImageName)
        image = pygame.image.load(pathname).convert_alpha()
        image = pygame.transform.scale(image, ImageSize)
        return image

    def __initPBImage(self, PassingByImageName):
        if PassingByImageName is None:
            return None
        pathname = os.path.join('image', 'button' ,PassingByImageName)
        image = pygame.image.load(pathname).convert_alpha()
        image = pygame.transform.scale(image, ImageSize)
        self.PBImage = image

    def display(self):
        if self.Image is None:
            return None
        #blank display

        if self.PBImage is None:
            self.Surface.blit(self.Image, (self.X,self.Y))
            return None

        if self.CheckClick(pygame.mouse.get_pos()):
            self.Surface.blit(self.PBImage, (self.X,self.Y))
        else:
            self.Surface.blit(self.Image, (self.X,self.Y))

    def CheckClick(self, postion):
        x = postion[0]
        y = postion[1]
        # bilt use top left corner
        if x < self.X or x > self.X + self.WIDTH or y < self.Y or y > self.Y + self.HEIGHT:
            return False
        else:
            return True

'''
TableArrange(number,interval_x,interval_y,(M*N),(SPostion)=(0,0))
for i in range(number)
tmp = i//M
postion(i) = (tmp , number - tmp*M)
P(i) = (tmp * interval_x + SPostion_X , (number - tmp * M)*interval_y + SPostion_Y)
'''
def TableArrange(number, interval_x, interval_y, table_x = 2, SPos_x = 0, SPos_y = 0):
    Table = []
    for i in range(number):
        tmp = i // table_x
        postion = (tmp * interval_x + SPos_x, (i - tmp * table_x)*interval_y + SPos_y)
        Table.append(postion)

    return Table

SCREEN_WIDTH = 1024
SCREEN_HEGIHT = 640
CWIDTH = 530
CHEIGHT = 530

def MulitiCharacterPostion(number):
    if number == 1:
        return [(220,110)]
    if number == 2:
        return [(50,110),(424,110)]

    interval = (SCREEN_WIDTH - CWIDTH) // (number - 1)

    MPos = []
    curpos = [10,110]
    for i in range(number):
        MPos.append(curpos.copy())
        curpos[0] = curpos[0] + interval
    return MPos
    
