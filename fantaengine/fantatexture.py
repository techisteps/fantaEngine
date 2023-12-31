from OpenGL.GL import *
import numpy as np
from PIL import Image
from typing import List

from icecream import ic


class fantaTexture:
    
    __texture: int = []
    __texture_details = {}
    
    @classmethod
    def getCount(cls):
        return len(fantaTexture.__texture)

    @classmethod
    def printAll(cls):
        print(fantaTexture.__texture)

    @classmethod
    def deleteAll(cls):
        li = []
        for k,v in fantaTexture.__texture_details.keys():
            li.append(k)
        glDeleteTextures(len(li), li)
        fantaTexture.__texture_details.clear()

        # glDeleteTextures(len(fantaTexture.__texture), fantaTexture.__texture)
        del fantaTexture.__texture[:]

    @staticmethod
    def setWrapandFilter(WS, WT, MinF, MaxF):
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, WS)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, WT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, MinF)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, MaxF)


    def genTex(self, i: int, name: str):
        self.tex = glGenTextures(i)
        fantaTexture.__texture.append(self.tex)
        fantaTexture.__texture_details[self.tex] = name
        glBindTexture(GL_TEXTURE_2D, self.tex)
        # ic(fantaTexture.__texture_details)
        # ic(self.__texture_details)

        # li = []
        # for k in fantaTexture.__texture_details.keys():
        #     li.append(k)
        # ic(li)

        
        

    def __init__(self, filepath: str = None):

        if filepath == "" or filepath is None:
            self.setChecker()
            return
        
        self.genTex(1, filepath)
        fantaTexture.setWrapandFilter(GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
        self.texture_ref = Image.open(filepath)
        self.texture_data = self.texture_ref.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.texture_ref.width, self.texture_ref.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)


    def setChecker(self):
        self.genTex(1, "checker")
        fantaTexture.setWrapandFilter(GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)
        checkerTex = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
                      1.0, 1.0, 1.0, 0.0, 0.0, 0.0]
        checkerTex = np.array(checkerTex, dtype=np.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 2, 2, 0, GL_RGB, GL_FLOAT, checkerTex)
        glBindTexture(GL_TEXTURE_2D, 0)


    def getTexID(self):
        return self.tex            