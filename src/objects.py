from error_list import error_dict_objects as object_errors
from error_list import error_dict_texture_group as texture_errors
from std_check_functions import collision_two_rectangles_no_rotation
import os
import pygame

# object_base_settings
# position (global perspective)
# dimensions (global perspective)

test_base_settings:list = [
    [540, 360], #position
    [100, 100], #dimensions   
]

test_base_settings2:list = [
    [590, 310],
    [100, 100]
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
    #__textures

    #variables set by class and function calls
    #__use_different_interaction_field
    #__interaction_field_size

    def __init__(self, object_base_settings:list, texGroup:textureGroup = None):
        #base settings handling
        self.__position:list[float, float] = object_base_settings[0]
        self.__dimensions:list[float, float] = object_base_settings[1]

        self.__textures:textureGroup = texGroup

        self.__use_different_interaction_field:bool = False
        self.__interaction_field:list[float, float] = None

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

    def use_other_interaction_field(self, use:bool):
        self.__use_different_interaction_field = use
    
    def is_using_other_interaction_field(self):
        return self.__use_different_interaction_field
    
    def set_other_interaction_field(self, field:list[int, int]):
        self.__interaction_field = field

    def get_other_interaction_field(self):
        return self.__interaction_field
    
    #main interraction check for in game things (like player walks in a zone)
    #first argument for function is always Mootor
    #create overrides for different arguments
    def game_interract(self, Mootor, function):
        if self.__use_different_interaction_field:
            pass
        else:
            cur_center = Mootor.get_current_center()
            cur_if_size = Mootor.get_interaction_field_size()

            iscol:bool = collision_two_rectangles_no_rotation([self.get_position(), self.get_dimensions()], 
                                                              [cur_center, cur_if_size], 
                                                              object1FromTopLeft=True)

            if iscol:
                function(Mootor)

    #main interraction check for ui objects (like player clicks a button in a menu)
    def ui_interrack(self):
        pass

    #main draw, drawType is for wether the draw should be textured or coloured
    def draw(self, screen:pygame.surface.Surface, drawType:str = "coloured", textureName:str = None):
        if drawType == "textured":
            if textureName != None:
                screen.blit(pygame.transform.scale(self.getTextureGroup().getTexture(textureName), self.get_dimensions()), 
                            self.get_position())
            else:
                raise Exception(object_errors[3])
        elif drawType != "coloured":
            raise Exception(object_errors[2])
        else:
            pygame.draw.rect(screen, self.getTextureGroup().getColour(), 
                             (tuple(self.get_position()), tuple(self.get_dimensions())))