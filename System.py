import pygame
import pickle
import time

'''
with open('saves.pkl','wb') as file :
    pickle.dump(parser.saver(), file)
'''
SAVESNUMBER = 6
PKLPATH = 'saves.pkl'

def initSavesPKL():
    SavesGroup = [None for i in range(SAVESNUMBER)]
    with open(PKLPATH,'wb') as file :
        pickle.dump(SavesGroup, file, 2)

class SavesControl(object):
    def __init__(self, parser):
        self.FilePath = PKLPATH
        self.SavesNumber = SAVESNUMBER
        #SavesGroup = [[saver,image] for i in range(self.SavesNumber)]

        self.Parser = parser
        self.Saved = self.__initSaved()

    def __initSaved(self):
        saved = [False for i in range(SAVESNUMBER)]
        with open(self.FilePath,'rb') as file :
            SavesGroup = pickle.load(file)
            for i in range(SAVESNUMBER):
                if SavesGroup[i] is not None:
                    saved[i] = True
        return saved


    def Save(self, saves_index, image):
        SavesGroup = None
        localtime = time.asctime( time.localtime(time.time()))
        with open(self.FilePath,'rb') as file :
            SavesGroup = pickle.load(file)
            SavesGroup[saves_index] = [self.Parser.saver(), pygame.image.tostring(image,'RGBA'), localtime]
        with open(self.FilePath,'wb') as file :
            pickle.dump(SavesGroup, file, 2)

    def Load(self, saves_index):
        with open(self.FilePath,'rb') as file :
            SavesGroup = pickle.load(file)
            if self.Saved[saves_index] == True:
                self.Parser.loader(SavesGroup[saves_index][0])

    def getImage(self, saves_index, size):
        if self.Saved[saves_index] == False:
            return None

        with open(self.FilePath,'rb') as file :
            SavesGroup = pickle.load(file)
            return pygame.image.fromstring(SavesGroup[saves_index][1], size, 'RGBA')

    def getTime(self, saves_index):
        if self.Saved[saves_index] == False:
            return None

        with open(self.FilePath,'rb') as file :
            SavesGroup = pickle.load(file)
            return SavesGroup[saves_index][2]