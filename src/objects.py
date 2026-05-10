from error_list import error_dict_objects as object_errors
from error_list import error_dict_texture_group as texture_errors
from std_check_functions import collision_two_rectangles_no_rotation
from std_check_functions import collision_mouse_rectangle_no_rotation
from std_check_functions import standardise_with_engine
import os
import pygame

# object_base_settings
# position (global perspective)
# dimensions (global perspective)

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
    #__game_interact_func
    #__ui_interact_func

    def __init__(self, object_base_settings:list, texGroup:textureGroup = None):
        #base settings handling
        self.__position:list[float, float] = object_base_settings[0]
        self.__dimensions:list[float, float] = object_base_settings[1]

        self.__textures:textureGroup = texGroup

        self.__use_different_interaction_field:bool = False
        self.__interaction_field:list[list[float, float]] = None

        self.__game_interact_func = None
        self.__ui_interact_func = None

        self.__draw_type = "coloured"

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
    
    #global just sets it according to the field[position, dimensions] variable
    #local sets interaction field from the field variable based on the current center of the object
    def set_other_interaction_field(self, field:list[list[int, int]], type:str = "global"):
        if type == "global":
            self.__interaction_field = field
        elif type == "local":
            cur_cen:list = [
                self.get_position()[0] + self.get_dimensions()[0],
                self.get_position()[1] + self.get_dimensions()[1]
            ]

            self.__interaction_field = [
                [
                    cur_cen[0] + field[0][0], cur_cen[1] + field[0][1]
                ],
                [
                    field[1][0], field[1][1]
                ]
            ]
        else:
            raise Exception(object_errors[4])
        
    #set the other interaction field size using [x, y] radius from the center
    def set_other_interaction_field_radius(self, radius:list[int, int]):
        #please help me i cant keep going any longer please this hurts
        cur_cen:list = [
            self.get_position()[0] + self.get_dimensions()[0],
            self.get_position()[1] + self.get_dimensions()[1]
        ]

        self.__interaction_field = [
            [
                cur_cen[0] - radius[0], cur_cen[1] - radius[1]
            ],
            [
                radius[0] * 2, radius[1] * 2
            ]
        ]

    def get_other_interaction_field(self):
        return self.__interaction_field
    
    def set_game_interact_func(self, function):
        self.__game_interact_func = function

    def get_game_interact_func(self):
        return self.__game_interact_func
    
    #main interraction check for in game things (like player walks in a zone)
    #first argument for function is always Mootor
    #create overrides for different arguments
    def game_interact(self, Mootor):
        cur_center = Mootor.get_current_center_fixed()
        cur_if_size = Mootor.get_interaction_field_size()

        if self.__use_different_interaction_field:
            iscol:bool = collision_two_rectangles_no_rotation(self.get_other_interaction_field(),
                                                              [cur_center, cur_if_size],
                                                              object1FromTopLeft=True)
        else:
            iscol:bool = collision_two_rectangles_no_rotation([self.get_position(), self.get_dimensions()], 
                                                              [cur_center, cur_if_size], 
                                                              object1FromTopLeft=True)

        if iscol and self.__game_interact_func != None:
            self.__game_interact_func(Mootor)

    #main interraction check for ui objects (like player clicks a button in a menu)
    def ui_interact(self, Mootor, function):
        pass

    def set_draw_type(self, drawType:str):
        self.__draw_type = drawType

    def get_draw_type(self):
        return self.__draw_type

    #main draw, drawType is for wether the draw should be textured or coloured
    def draw(self, Mootor, textureName:str = None):
        if self.__draw_type == "textured":
            if textureName != None:
                Mootor.get_screen().blit(pygame.transform.scale(self.getTextureGroup().getTexture(textureName), self.get_dimensions()), 
                            standardise_with_engine(self.get_position(), Mootor.get_current_center()))
            else:
                raise Exception(object_errors[3])
        elif self.__draw_type != "coloured":
            raise Exception(object_errors[2])
        else:
            pygame.draw.rect(Mootor.get_screen(), self.getTextureGroup().getColour(), 
                             (tuple(standardise_with_engine(self.get_position(), Mootor.get_current_center())),
                              tuple(self.get_dimensions())))