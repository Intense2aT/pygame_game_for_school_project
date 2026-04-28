from error_list import error_dict_objects as object_errors
import os
import pygame

# object_base_settings
# position (global perspective)
# dimensions (global perspective)

test_base_settings:list = [
    [0, 0], #position
    [100, 100], #dimensions   
]

# object_texture_settings
# textured / coloured / both
# both is used if nothing is specified

test_display_settings:list = [
    "both",
    #texture settings (for texture and both)
    "heartPixel1.png",
    #colour settings (for colour and both)
    (0xFF, 0x40, 0xFF, 0xFF), #RGBA colour
    #both
    "textured", #draw priority (which is drawin on top if possible)
]


#normal 2d object
class object:
    #variables set by init
    #__position
    #__dimensions
    def __handle_texture_init(self, path_from_textures_folder:str):
        self.__texture_image = pygame.image.load(os.path.join('textures', path_from_textures_folder))

    def __handle_colour_init(self, colour:tuple[int, int, int, int]):
        self.__colour = colour

    def __init__(self, object_base_settings:list, object_display_settings:list = None):
        #base settings handling
        self.__position:list[float, float] = object_base_settings[0]
        self.__dimensions:list[float, float] = object_base_settings[1]

        #display settings handling
        if object_display_settings != None:
            if object_display_settings[0] == "textured":
                self.__handle_texture_init(object_display_settings[1])
            elif object_display_settings[0] == "coloured":
                self.__handle_colour_init(object_display_settings[2])
            else:
                self.__handle_texture_init(object_display_settings[1])
                self.__handle_colour_init(object_display_settings[2])
                self.__draw_priority:str = object_display_settings[3]

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
    
    #main interraction check for in game things (like player walks in a zone)
    def game_interract():
        pass

    #main interraction check for ui objects (like player clicks a button in a menu)
    def ui_interrack():
        pass

    #main draw
    def draw():
        pass