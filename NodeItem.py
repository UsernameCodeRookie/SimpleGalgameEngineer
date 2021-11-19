import pygame
import os
import util
import copy
import time
from pygame.locals import *

ALPHA = 140
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
TEXTRECT_HIGHT = 200
LINE_NUMBER = 30
TEXTOFFX = 60
TEXTOFFY = 20
LINESPACING = 30
CPOSX = 220
CWIDTH = 530
CHEIGHT = 530

THUMBNAIL_WIDTH = 256
THUMBNAIL_HEIGHT = 160

MAXCHARACTER = 5

class NodeItem(object):

    def __init__(self, surface):
        self.BGMName = ''
        self.Background = ''
        self.CharacterName = ''
        self.MultiCharacter = [None for i in range(MAXCHARACTER)]
        self.MultiCharacterImage = [None for i in range(MAXCHARACTER)]
        self.MultiCharacterNumber = 1
        self.Text = ''

        self.Surface = surface
        self.CharacterPos = None
        self.TextColor = ((221, 231, 35))
        self.TextBoxColor = ((0, 0, 0))
        self.TextBoxPos = (0, SCREEN_HEIGHT - TEXTRECT_HIGHT)
        self.TextBox, self.TextBoxRect = self.__initTextRect()
        self.TextBoxSize = (SCREEN_WIDTH, TEXTRECT_HIGHT)
        self.Font = self.__initFont()

        self.SaveButton = util.Button(self.Surface, (800,620), ImageName='save.jpg')
        self.LoadButton = util.Button(self.Surface, (840,620), ImageName='load.jpg')
        self.DisplayButtonGroup = [self.SaveButton, self.LoadButton]

    def __initTextRect(self, colorkey = ALPHA):
        size = (SCREEN_WIDTH, TEXTRECT_HIGHT)
        TextRect = pygame.Surface(size)
        TextRect.fill(self.TextBoxColor)

        if colorkey is not None:
            TextRect.set_alpha(colorkey)
        return TextRect, TextRect.get_rect()

    def __initFont(self, name = 'msyh.ttf', size = 20):
        #pathname = os.path.join('font',name)
        #Font = pygame.font.Font(pathname, size)
        Font = pygame.font.SysFont('SimHei', size)
        return Font

    def update(self, parser):
        self.__updateBGM(parser.getBGM())
        self.__updateBackground(parser.getBackground())
        self.__updateMultiCharacter(parser.getMultiCharacter())
        self.__updateCharacter(parser.getCharacterName())
        self.__updateText(parser.getText())


    def __updateBackground(self, name, colorkey = None):
        if name == '':
            return None

        pathname = os.path.join('image', 'background' ,name)
        image = pygame.image.load(pathname).convert()
        image = pygame.transform.scale(image,(SCREEN_WIDTH,SCREEN_HEIGHT))
        self.Background = image
        self.Surface.blit(image,(0,0))

    def __updateBGM(self, name):
        if name =='':return
        class NoneSound:
            def play(self):pass
        if not pygame.mixer:
            return NoneSound()
        pathname = os.path.join('bgm', name)
        if self.BGMName == pathname:
            return 
        pygame.mixer.music.load(pathname)
        self.BGMName = pathname
        self.play()

    def __updateMultiCharacter(self, multi_character):
        self.MultiCharacter = multi_character
        self.MultiCharacterNumber = len(multi_character)
        #could be zero
        self.CharacterPos = util.MulitiCharacterPostion(self.MultiCharacterNumber)

        for i in range(self.MultiCharacterNumber):
            name = self.MultiCharacter[i] + '.png'
            pathname = os.path.join('image', 'character' ,name)
            image = pygame.image.load(pathname).convert_alpha()
            image = pygame.transform.scale(image,(CWIDTH,CHEIGHT))
            self.MultiCharacterImage[i] = image


    def __updateCharacter(self, character_name, colorkey=None):

        Mask = pygame.Surface((CWIDTH,CHEIGHT))
        Mask.fill((70, 70, 70))

        self.CharacterName = character_name

        for i in range(self.MultiCharacterNumber):
            if self.MultiCharacter[i] != character_name:
                image = self.MultiCharacterImage[i].copy()
                image.blit(Mask,(0,0),special_flags = BLEND_RGBA_MULT)
                self.Surface.blit(image,self.CharacterPos[i])

        for i in range(self.MultiCharacterNumber):
            if self.MultiCharacter[i] == character_name:
                image = self.MultiCharacterImage[i].copy()
                self.Surface.blit(image,self.CharacterPos[i])


    def __updateText(self, text, colorkey = ALPHA):
        self.TextBox.fill(self.TextBoxColor)
        if colorkey is not None:
            self.TextBox.set_alpha(colorkey)
        #refresh
        self.Surface.blit(self.TextBox,self.TextBoxPos)

        if text[-1] == '\n':
            self.Text = text[:-1]
        else:
            self.Text = text

        textLines = [self.Text[i:i+LINESPACING] for i in range(len(text)) if i % LINESPACING == 0]

        name = ''
        if self.CharacterName !='':
            name =self.CharacterName+':'
        textLines.insert(0,name)


        for lineNum in range(len(textLines)):
            currentLine = textLines[lineNum]
            fontSurface = self.Font.render(currentLine,True,self.TextColor)
            xPos = TEXTOFFX
            yPos = TEXTOFFY + lineNum * LINESPACING + SCREEN_HEIGHT - TEXTRECT_HIGHT
            self.Surface.blit(fontSurface,(xPos,yPos))

        #https://pythonhosted.org/kitchen/api-text-display.html

    def ButtonGroupDisplay(self):
        for button in self.DisplayButtonGroup:
            button.display()

    def EventCheckClick(self):
        return



    '''
    SaveLoadInterface:
    One background, four(undetermined) thumbnails
    '''
class SaveLoadInterface(object):
    def __init__(self, surface, saves_control = None):
        self.Background = self.__initBackground()
        self.Surface = surface
        self.SavesControl = saves_control

        self.SLmode = 'save'
        self.ScreenShotImage = None

        self.ThumbnailSize = (THUMBNAIL_WIDTH,THUMBNAIL_HEIGHT)
        self.__ThumbnailNum = 6
        self.__DefaultThumbnail = pygame.image.load('image/others/DefaultThumbnail.jpg').convert()

        self.ThumbnailGroup = self.__initThumbnailGroup()

        self.ExitButton = util.Button(self.Surface, (800,620), ImageName='exit.jpg')
        self.DisplayButtonGroup = [self.ExitButton]

    def __initBackground(self, SLBackground = 'SLBackground.jpg'):
        if SLBackground == '':
            return None

        pathname = os.path.join('image', 'background' ,SLBackground)
        image = pygame.image.load(pathname).convert()
        image = pygame.transform.scale(image,(SCREEN_WIDTH,SCREEN_HEIGHT))
        return image


    def __initThumbnailGroup(self):
        Group = []
        table =util.TableArrange(self.__ThumbnailNum, 300, 200, 2, 100, 50)
        for i in range(self.__ThumbnailNum):
            tmp = util.Button(self.Surface, table[i], 'DefaultThumbnail.jpg', self.ThumbnailSize)
            if self.SavesControl.Saved[i] == True :
                tmp.Image = self.SavesControl.getImage(i, self.ThumbnailSize)
            Group.append(tmp)
        return Group

    def update(self):
        if self.Background is not None:
            self.Surface.blit(self.Background, (0,0))

        for i in range(self.__ThumbnailNum):
            self.ThumbnailGroup[i].display()

        self.ButtonGroupDisplay()

    #mouse passby graphic effect
    def SetPBImage(self, image = None):
        #Mask
        Mask = pygame.Surface(self.ThumbnailSize)
        Mask.fill((0xFF, 0xFF, 0xFF))
        Mask.set_alpha(40)

        if self.SLmode == 'save' :
            tmp = pygame.transform.scale(image,self.ThumbnailSize)
            self.ScreenShotImage = tmp.copy()
            tmp.blit(Mask,(0,0))
            for i in range(self.__ThumbnailNum):
                self.ThumbnailGroup[i].PBImage = tmp

        elif self.SLmode == 'load' :
            for i in range(self.__ThumbnailNum):
                if self.SavesControl.Saved[i] == True :
                    tmp = self.SavesControl.getImage(i, self.ThumbnailSize)
                else:
                    tmp = self.__DefaultThumbnail
                    tmp = pygame.transform.scale(tmp, self.ThumbnailSize)
                tmp.blit(Mask,(0,0))
                self.ThumbnailGroup[i].PBImage = tmp

    #SLmode = 'save' or 'load'
    # if load return true
    def EventCheckClick(self, mouse_postion):
        for i in range(self.__ThumbnailNum):
            if self.ThumbnailGroup[i].CheckClick(mouse_postion):
                if self.SLmode == 'save':
                    self.ThumbnailGroup[i].Image = self.ScreenShotImage
                    self.SavesControl.Save(i, self.ScreenShotImage)
                else:
                    if self.SavesControl.Saved[i]:
                        self.SavesControl.Load(i)
                        return True
                return False

    def ButtonGroupDisplay(self):
        for button in self.DisplayButtonGroup:
            button.display()
