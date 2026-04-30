from error_list import error_dict_objects as object_errors
from error_list import error_dict_texture_group as texture_errors
import os
import pygame

# object_base_settings
# position (global perspective)
# dimensions (global perspective)

test_base_settings:list = [
    [0, 0], #position
    [100, 100], #dimensions   
]

class textureGroup:
    def __init__(self, colour:tuple[int, int, int, int] = None):
        self.__texture_dict:dict = {}
        self.__colour = colour

    def setColour(self, colour:tuple[int, int, int, int]):
        self.__colour = colour

    def getColour(self):
        return self.__colour
    
    #name = name in map, filepath for loading
    def addTexture(self, name:str, filepath:str, overWriteExisting:bool = True):
        if overWriteExisting:
            self.__texture_dict[name] = pygame.image.load(filepath)
        else:
            if name in self.__texture_dict.keys():
                raise Exception(texture_errors[1])
            else:
                self.__texture_dict[name] = pygame.image.load(filepath)

    def getTexture(self, name:str):
        if name in self.__texture_dict.keys():
            return self.__texture_dict[name]
        else:
            raise Exception(texture_errors[2])

#normal 2d object
class object:
    #variables set by init
    #__position
    #__dimensions

    def __init__(self, object_base_settings:list, texGroup:textureGroup = None):
        #base settings handling
        self.__position:list[float, float] = object_base_settings[0]
        self.__dimensions:list[float, float] = object_base_settings[1]

        self.__textures:textureGroup = texGroup

    def get_position(self) -> list[float, float]:
        return self.__position
    
    def set_position(self, new_position:list[float, float]):
        self.__position = new_position

    #2d move vector
    def move_position(self, move_vector:list[float, float]):
        self.__position[0] += move_vector[0]
        self.__position[1] += move_vector[1]

    def get_dimensions(self) -> list[float, float]:
        return self.__dimensions
    
    def set_dimmensions(self, new_dimensions:list[float, float]):
        self.__dimensions = new_dimensions

    #Value after adjustment for either x or y can NOT be negative
    def adjust_dimensions(self, adjustment_vector:list[float, float]):
        for i in range(0, 2):
            if self.__dimensions[i] + adjustment_vector[i] > 0:
                self.__dimensions[i] += adjustment_vector[i]
            else:
                raise Exception(object_errors[1])
            
    def getTextureGroup(self):
        return self.__textures
    
    def setTextureGroup(self, texGroup:textureGroup):
        self.__textures = texGroup
    
    #main interraction check for in game things (like player walks in a zone)
    def game_interract(self):
        pass

    #main interraction check for ui objects (like player clicks a button in a menu)
    def ui_interrack(self):
        pass

    #main draw, drawType is for wether the draw should be textured or coloured
    def draw(self, screen:pygame.Surface, drawType:str = "coloured"):
        if drawType == "textured":
            pass
        elif drawType != "coloured":
            raise Exception(object_errors[2])
        else:
            pass