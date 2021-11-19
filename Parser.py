import re

'''
background: (background.jpg)
music: (music.mp3)
text: Name:Text
'''

class Parser(object):
    def __init__(self, script):
        self.Index = -1
        # index of the sentence for S/L
        self.Background = ''
        self.CharacterName = ''
        
        self.Text = ''
        self.BGM = ''

        self.MultiCharacter = []

        # constant
        self.Script = script
        self.RPBackground = self.__InitRPBackground()
        self.RPText = self.__InitRPText()
        self.RPBGM = self.__InitRPBGM()
        self.RPMultiCharacter = self.__initRPMultiCharacter()

    def __InitRPBackground(self):
        pattern = r'^\((.+?)\.jpg\)$'
        return re.compile(pattern,re.M)

    def __InitRPText(self):
        pattern = r'^(.+?):(.+?)$'
        return re.compile(pattern,re.M)

    def __InitRPBGM(self):
        pattern = r'^\((.+?)\.mp3\)$'
        return re.compile(pattern,re.M)

    def __initRPMultiCharacter(self):
        pattern = r'^\<(.+?)\>$'
        return re.compile(pattern,re.M)

    def parserTarget(self, target):

        if self.RPBackground.search(target):
            self.Background = self.RPBackground.search(target).group(1) + '.jpg'
            self.MultiCharacter = []
            self.NextIndex()
        elif self.RPBGM.search(target):
            self.BGM = self.RPBGM.search(target).group(1) + '.mp3'
            self.NextIndex()
        elif self.RPText.search(target):
            tmp = target.split(':')
            self.CharacterName = tmp[0]
            self.Text = tmp[1]
        elif self.RPMultiCharacter.search(target):
            tmp = target[1:-2]
            self.MultiCharacter = tmp.split(',')
            self.NextIndex()
        else:
            self.Text = target

    def NextIndex(self):
        self.Index = self.Index + 1
        self.parserTarget(self.Script[self.Index])

    def getBackground(self):
        return self.Background

    def getBGM(self):
        return self.BGM

    def getCharacterName(self):
        return self.CharacterName

    def getText(self):
        return self.Text

    def getMultiCharacter(self):
        return self.MultiCharacter

    #useless and ugly
    def saver(self):
        return [self.Index,self.Background,self.CharacterName,self.Text,self.BGM,self.MultiCharacter]

    def loader(self,saver):
        self.Index,self.Background,self.CharacterName,self.Text,self.BGM,self.MultiCharacter = saver