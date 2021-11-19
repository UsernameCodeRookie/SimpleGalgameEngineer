import pygame
import os
import Parser
import NodeItem
import sys
import util
import System
from pygame.locals import *

# 1366*768
# 1024*640
pygame.init()
size = (1024, 640)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

#System.initSavesPKL()

pygame.display.set_caption('Test')
script = []
with open('test.txt',encoding='utf-8') as ScriptFile:
    for line in ScriptFile:script.append(line)
parser = Parser.Parser(script)
nodeitem = NodeItem.NodeItem(screen)
saves_control = System.SavesControl(parser)
saveload_interface = NodeItem.SaveLoadInterface(screen, saves_control)

TextBoxClickCheck = util.Button(screen, (100,460), None, (800,160))

#StateControl
parser.NextIndex()
nodeitem.update(parser)
State = 'PlayState'
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
                exit()

        if State == 'PlayState' :
            nodeitem.ButtonGroupDisplay()

            if event.type == MOUSEBUTTONDOWN:

                MousePostion = pygame.mouse.get_pos()

                if TextBoxClickCheck.CheckClick(MousePostion):
                    parser.NextIndex()
                    nodeitem.update(parser)

                if nodeitem.SaveButton.CheckClick(MousePostion):
                    ScreenShot = screen.copy()
                    saveload_interface.SLmode = 'save'
                    saveload_interface.SetPBImage(ScreenShot)
                    State = 'SaveLoadState'

                if nodeitem.LoadButton.CheckClick(MousePostion):
                    saveload_interface.SLmode = 'load'
                    saveload_interface.SetPBImage()
                    State = 'SaveLoadState'

                nodeitem.EventCheckClick()

        elif State == 'SaveLoadState' :
            saveload_interface.update()

            if event.type == MOUSEBUTTONDOWN:
                MousePostion = pygame.mouse.get_pos()
                if(saveload_interface.EventCheckClick(MousePostion)):
                    State = 'PlayState'
                    nodeitem.update(parser)

                if(saveload_interface.ExitButton.CheckClick(MousePostion)):
                    State = 'PlayState'
                    nodeitem.update(parser)

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    State = 'PlayState'
                    nodeitem.update(parser)

    clock.tick(60)
    pygame.display.update()
