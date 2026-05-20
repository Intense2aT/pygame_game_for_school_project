from error_list import error_dict_objects as object_errors
from error_list import error_dict_texture_group as texture_errors
from std_check_functions import collision_two_rectangles_no_rotation
from std_check_functions import collision_mouse_rectangle_no_rotation
from std_check_functions import standardise_with_engine
import os
import json
import pygame

# object_base_settings
# position (global perspective)
# dimensions (global perspective)

class textureGroup:
    def __init__(self):
        self.__texture_dict:dict = {}
        self.__colour_dict:dict = {}
        self.__font_dict:dict = {}

    def get_texture_group(self):
        return self.__texture_dict

    def load_from_json(self, filepath:str, clear_all:bool = True):
        file = open(filepath, 'r')
        data = json.load(file)

        if clear_all:
            self.__texture_dict:dict = {}
            self.__colour_dict:dict = {}
            self.__font_dict:dict = {}

        for global_key in data.keys():
            for item in data[global_key]:
                if global_key == "colours":
                    self.__colour_dict[item] = data[global_key][item]
                elif global_key == "textures":
                    self.__texture_dict[item] = pygame.image.load(data[global_key][item]).convert_alpha()
                elif global_key == "fonts":
                    self.__font_dict[item] = pygame.font.Font(data[global_key][item][0],
                                                              data[global_key][item][1])

    def addColour(self, name:str, colour:tuple[int, int, int, int], overWriteExisting:bool = True):
        if overWriteExisting:
            self.__colour_dict[name] = colour
        else:
            if name in self.__colour_dict.keys():
                raise Exception(texture_errors[5])
            else:
                self.__colour_dict[name] = colour

    def getColour(self, name:str):
        if name in self.__colour_dict.keys():
            return self.__colour_dict[name]
        else:
            raise Exception(texture_errors[6])
    
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
        
    def addFont(self, name:str, filepath:str, size:int, overWriteExisting:bool = True):
        if overWriteExisting:
            self.__font_dict[name] = pygame.font.Font(filepath, size)
        else:
            if name in self.__font_dict.keys():
                raise Exception(texture_errors[3])
            else:
                self.__font_dict[name] = pygame.font.Font(filepath, size)

    def getFont(self, name:str):
        if name in self.__font_dict.keys():
            return self.__font_dict[name]
        else:
            raise Exception(texture_errors[4])

#normal 2d object
class object:
    #variables set by init
    #__position
    #__dimensions
    #__textures
    #__responsive_mouse_button

    #variables set by class and function calls
    #__use_different_interaction_field
    #__interaction_field_size
    #__game_interact_func
    #__ui_interact_func

    def __init__(self, object_base_settings:list, texGroup:textureGroup = None):
        #base settings handling
        self.__position:list[float, float] = object_base_settings[0]
        self.__dimensions:list[float, float] = object_base_settings[1]
        self.__rotation:float = 0.0
        
        #for drawing a grid of equal sized objects
        #grid will still use the top left position of the grid for position
        self.__grid_draw:bool = False
        self.__grid_dimensions:list[int, int] = None
        self.__differentiated_points:dict = {}
        self.__grid_surface_prerender:pygame.surface.Surface = None
        #could make a special grid type later for different textures in one grid
        #could also add the option for multiple seperately defined intearactionfields related to one object

        self.__textures:textureGroup = texGroup

        self.__use_different_interaction_field:bool = False
        self.__interaction_field:list[list[float, float]] = None
        self.__texture_size_fix:list[list[float, float]] = None
        self.__draw_field_under_object:bool = False

        self.__game_interact_func = None
        self.__ui_interact_func = None

        self.__responsive_mouse_button:int = 1
        #always calls func if button is pressed, otherwise calls only once
        self.__respond_continuous:bool = False
        #calls func when button is pressed, otherwise calls on release
        self.__call_on_press:bool = False

        self.__draw_type:str = "coloured"
        self.__colour_name:str = None
        self.__texture_name:str = None

        self.__draw_with_text:bool = False
        self.__text_to_draw:str = None
        self.__text_colour_name:str = None
        self.__text_dimensions:list[float, float] = self.__dimensions
        self.__text_position:list[float, float] = [self.__position[0], self.__position[1]]
        self.__rendered_text:pygame.surface.Surface = None


    def load_from_json(self, filepath:str):
        file = open(filepath, 'r')
        data = json.load(file)

        for key in data.keys():
            if key == "position":
                self.set_position(data[key])
            elif key == "dimensions":
                self.set_dimensions(data[key])
            elif key == "rotation":
                self.set_rotation(data[key])
            elif key == "grid_draw":
                self.set_grid_draw(data[key])
            elif key == "grid_dimensions":
                self.set_grid_dimensions(data[key])
            elif key == "use_different_interaction_field":
                self.use_other_interaction_field(data[key])
            elif key == "interaction_field":
                self.set_other_interaction_field(data[key])
            elif key == "draw_field_under_object":
                self.set_draw_field_under_object(data[key])
            elif key == "responsive_mouse_button":
                self.set_responsive_mouse_button(data[key])
            elif key == "respond_continuous":
                self.set_respond_continuous(data[key])
            elif key == "call_on_press":
                self.set_call_on_press(data[key])
            elif key == "draw_type":
                self.set_draw_type(data[key])
            elif key == "colour_name":
                self.set_colour_name(data[key])
            elif key == "texture_name":
                self.set_texture_name(data[key])
            elif key == "draw_with_text":
                self.set_draw_with_text(data[key])
            elif key == "text_to_draw":
                self.set_text_to_draw(data[key])
            elif key == "text_colour_name":
                self.set_text_colour_name(data[key])

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
    
    def set_dimensions(self, new_dimensions:list[float, float]):
        self.__dimensions = new_dimensions

    def set_rotation(self, deg:float):
        self.__rotation = deg

    def get_rotation(self):
        return self.__rotation

    def set_grid_draw(self, set:bool):
        self.__grid_draw = set

    def get_grid_draw(self):
        return self.__grid_draw
    
    def set_grid_dimensions(self, dims:list[int, int]):
        self.__grid_dimensions = dims

    def get_grid_dimensions(self):
        return self.__grid_dimensions

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

    def set_interaction_field_for_grid(self):
        self.__interaction_field = [
            #FUCK PYTHON I DO NOT WANT THIS PASSED BY REFERENCE
            [
                self.__position[0],
                self.__position[1]
            ],
            [
                self.__dimensions[0] * self.__grid_dimensions[0],
                self.__dimensions[1] * self.__grid_dimensions[1]
            ]
        ]

    def fix_interaction_field_to_texture(self, tex_size:int):
        self.__interaction_field[0][1] += self.get_dimensions()[1] / tex_size * self.__texture_size_fix[0][0]
        self.__interaction_field[1][1] -= self.get_dimensions()[1] / tex_size * self.__texture_size_fix[0][1]
        self.__interaction_field[0][0] += self.get_dimensions()[0] / tex_size * self.__texture_size_fix[1][0]
        self.__interaction_field[1][0] -= self.get_dimensions()[0] / tex_size * self.__texture_size_fix[1][1]

    def get_other_interaction_field(self):
        return self.__interaction_field
    
    def set_texture_size_fix(self, adjustment:list[float, float]) -> None:
        self.__texture_size_fix = adjustment

    def get_texture_size_fix(self):
        return self.__texture_size_fix
    
    def set_draw_field_under_object(self, set:bool) -> None:
        self.__draw_field_under_object = set

    def get_draw_field_under_object(self) -> bool:
        return self.__draw_field_under_object
    
    def set_game_interact_func(self, function):
        self.__game_interact_func = function

    def get_game_interact_func(self):
        return self.__game_interact_func
    
    def set_ui_interact_func(self, function):
        self.__ui_interact_func = function

    def get_ui_interact_func(self):
        return self.__ui_interact_func
    
    def set_responsive_mouse_button(self, button:int):
        self.__responsive_mouse_button = button

    def get_responsive_mouse_button(self):
        return self.__responsive_mouse_button
    
    def set_respond_continuous(self, set:bool):
        self.__respond_continuous = set

    def get_respond_continuous(self):
        return self.__respond_continuous
    
    def set_call_on_press(self, set:bool):
        self.__call_on_press = set

    def get_call_on_press(self):
        return self.__call_on_press

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
    def ui_interact(self, Mootor):
        mouse_local = Mootor.get_cur_mouse_position()

        if mouse_local == None:
            #print("waiting for mouse to appear")
            return
        
        mouse_global = [
            mouse_local[0] + Mootor.get_current_global_pos()[0],
            mouse_local[1] + Mootor.get_current_global_pos()[1]
        ]

        if self.__use_different_interaction_field:
            iscol:bool = collision_mouse_rectangle_no_rotation(self.get_other_interaction_field(),
                                                               mouse_global,
                                                               objectFromTopLeft=True)
        else: 
            iscol:bool = collision_mouse_rectangle_no_rotation([self.get_position(), self.get_dimensions()],
                                                               mouse_global,
                                                               objectFromTopLeft=True)
            
        if not iscol: return

        mouse_states_cur = Mootor.get_cur_mousebutton_states()
        mouse_states_prev = Mootor.get_prev_mousebutton_states()
        if self.__call_on_press:
            if mouse_states_cur[self.__responsive_mouse_button - 1] == True:
                if self.__respond_continuous:
                    if self.__ui_interact_func != None:
                        self.__ui_interact_func(Mootor)
                else:
                    if mouse_states_prev[self.__responsive_mouse_button - 1] == False and self.__ui_interact_func != None:
                        self.__ui_interact_func(Mootor)
        else:
            if mouse_states_cur[self.__responsive_mouse_button - 1] == False:
                if self.__respond_continuous:
                    if self.__ui_interact_func != None:
                        self.__ui_interact_func(Mootor)
                else:
                    if mouse_states_prev[self.__responsive_mouse_button - 1] == True and self.__ui_interact_func != None:
                        self.__ui_interact_func(Mootor)

    def set_draw_type(self, drawType:str):
        self.__draw_type = drawType

    def get_draw_type(self):
        return self.__draw_type
    
    def set_texture_name(self, textureName:str):
        self.__texture_name = textureName

    def get_texture_name(self):
        return self.__texture_name
    
    def set_colour_name(self, colourName:str):
        self.__colour_name = colourName

    def get_colour_name(self):
        return self.__colour_name
    
    def set_draw_with_text(self, set:bool):
        self.__draw_with_text = set

    def get_draw_with_text(self):
        return self.__draw_with_text
    
    def set_text_to_draw(self, text:str):
        self.__text_to_draw = text
        #QUICKFIX, THIS IS BAD FIX SCALING LATER
        print("Text scaling bad fix applied in set_text_to_draw() func in object")
        self.__text_to_draw = self.__text_to_draw + ' '

    def get_text_to_draw(self):
        return self.__text_to_draw
    
    def set_text_colour_name(self, name:str):
        self.__text_colour_name = name

    def get_text_colour_name(self):
        return self.__text_colour_name
    
    def set_text_dimensions(self, dimensions:list[float, float]):
        self.__text_dimensions = dimensions

    def set_text_dimensions_scale_rel(self, x_mul:float, y_mul:float):
        self.__text_dimensions = [
            self.__dimensions[0] * x_mul,
            self.__dimensions[1] * y_mul
        ]

    def get_text_dimensions(self):
        return self.__text_dimensions
    
    #start and end according to python list standards
    def update_rendered_text(self, fontName:str, AA:bool = 0, start:int = 0, end:int = 0):
        if end == 0:
            end = len(self.__text_to_draw) - 1
        elif end > len(self.__text_to_draw) - 1:
            raise Exception(object_errors[5])

        text = self.__text_to_draw[start:end]
        if self.__text_colour_name == None:
            raise Exception(object_errors[9])
        self.__rendered_text = self.__textures.getFont(fontName).render(text, AA, self.__textures.getColour(self.__text_colour_name))

    def center_text(self, center_x:bool = True, center_y:bool = True):
        if not self.__grid_draw:
            if center_x:
                self.__text_position[0] = self.__position[0] + (self.__dimensions[0] - self.__text_dimensions[0]) / 2

            if center_y:
                self.__text_position[1] = self.__position[1] + (self.__dimensions[1] - self.__text_dimensions[1]) / 2
        else:
            if self.__grid_dimensions == None:
                raise Exception(object_errors[7])

            if center_x:
                self.__text_position[0] = self.__position[0] + (self.__dimensions[0] * self.__grid_dimensions[0] - self.__text_dimensions[0]) / 2

            if center_y:
                self.__text_position[1] = self.__position[1] + (self.__dimensions[1] * self.__grid_dimensions[1] - self.__text_dimensions[1]) / 2

    def add_differentiated_grid_point(self, positionStr:str, textureName:str, override:bool = True):
        if not (0 < int(positionStr.split('/')[0]) <= self.__grid_dimensions[0]): raise Exception("Can't add other grid point, position X value not in grid")
        if not (0 < int(positionStr.split('/')[1]) <= self.__grid_dimensions[1]): raise Exception("Can't add other grid point, position Y value not in grid")

        if positionStr not in self.__differentiated_points.keys():
            self.__differentiated_points[positionStr] = textureName
        elif override:
            self.__differentiated_points[positionStr] = textureName
        else:
            raise Exception(object_errors[10])

    def prerender_grid(self, use_redefined_points:bool = True):
        self.__grid_surface_prerender = pygame.Surface([self.__grid_dimensions[0] * self.__dimensions[0],
                                                        self.__grid_dimensions[1] * self.__dimensions[1]], pygame.SRCALPHA, 32)
        
        drawn_object = pygame.transform.scale(self.getTextureGroup().getTexture(self.__texture_name), self.get_dimensions())

        if use_redefined_points:
            for x in range(0, self.__grid_dimensions[0]):
                for y in range(0, self.__grid_dimensions[1]):
                    key = (str(x + 1) + '/' + str(y + 1))
                    if key in self.__differentiated_points.keys():
                        drawn_object = pygame.transform.scale(self.getTextureGroup().getTexture(self.__differentiated_points[key]), self.get_dimensions())
                        self.__grid_surface_prerender.blit(drawn_object, (self.__dimensions[0] * x, self.__dimensions[1] * y))
                        drawn_object = pygame.transform.scale(self.getTextureGroup().getTexture(self.__texture_name), self.get_dimensions())
                    else:
                        self.__grid_surface_prerender.blit(drawn_object, (self.__dimensions[0] * x, self.__dimensions[1] * y))
        else:
            for x in range(0, self.__grid_dimensions[0]):
                for y in range(0, self.__grid_dimensions[1]):
                    self.__grid_surface_prerender.blit(drawn_object, (self.__dimensions[0] * x, self.__dimensions[1] * y))

    #main draw, drawType is for wether the draw should be textured or coloured
    def draw(self, Mootor):
        if self.__draw_field_under_object:
            if self.__colour_name != None:
                pygame.draw.rect(Mootor.get_screen(), self.getTextureGroup().getColour(self.__colour_name), 
                                 (tuple(standardise_with_engine(self.get_other_interaction_field()[0], Mootor.get_current_global_pos())),
                                  tuple(self.get_other_interaction_field()[1])))
            else:
                raise Exception(object_errors[8])

        if self.__draw_type == "textured":
            if self.__texture_name != None:
                if self.__grid_draw:
                    if self.__grid_dimensions == None:
                        raise Exception(object_errors[7])
                    else:
                        if self.__grid_surface_prerender != None:
                            Mootor.get_screen().blit(pygame.transform.rotate(self.__grid_surface_prerender, self.__rotation), standardise_with_engine(self.get_position(), Mootor.get_current_global_pos()))
                        else:
                            drawn_object = pygame.transform.scale(self.getTextureGroup().getTexture(self.__texture_name), self.get_dimensions())
                            true_cords = standardise_with_engine(self.get_position(), Mootor.get_current_global_pos())
                            draw_list:list = []

                            for i in range(0, self.__grid_dimensions[0]):
                                for j in range(0, self.__grid_dimensions[1]):
                                    draw_list.append((drawn_object,
                                                    (true_cords[0] + self.__dimensions[0] * i,
                                                    true_cords[1] + self.__dimensions[1] * j)))
                            Mootor.get_screen().blits(draw_list)
                else:
                    Mootor.get_screen().blit(pygame.transform.rotate(pygame.transform.scale(self.getTextureGroup().getTexture(self.__texture_name), self.get_dimensions()), self.__rotation), 
                                             standardise_with_engine(self.get_position(), Mootor.get_current_global_pos()))
            else:
                raise Exception(object_errors[3])
        elif self.__draw_type != "coloured":
            raise Exception(object_errors[2])
        else:
            if self.__colour_name != None:
                pygame.draw.rect(Mootor.get_screen(), self.getTextureGroup().getColour(self.__colour_name), 
                                 (tuple(standardise_with_engine(self.get_position(), Mootor.get_current_global_pos())),
                                  tuple(self.get_dimensions())))
            else:
                raise Exception(object_errors[8])
            
        if self.__draw_with_text:
            if self.__rendered_text != None:
                final_renderable_surface = pygame.transform.rotate(pygame.transform.scale(self.__rendered_text, self.get_text_dimensions()), self.__rotation)
                Mootor.get_screen().blit(final_renderable_surface,
                                         standardise_with_engine(self.__text_position, Mootor.get_current_global_pos()))
            else:
                raise Exception(object_errors[6])
            
class player(object):
    def center_on_screen(self, mootor):
        self.set_position([mootor.get_current_center_fixed()[0] - self.get_dimensions()[0] / 2,
                           mootor.get_current_center_fixed()[1] - self.get_dimensions()[1] / 2])

    def set_move_speed(self, speed:float):
        self.__player_speed = speed

    def get_player_speed(self):
        return self.__player_speed
    
    def set_dir_vector(self, vector:list[int, int]):
        self.__player_move_direction = vector

    def get_dir_vector(self):
        return self.__player_move_direction