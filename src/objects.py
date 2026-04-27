from error_list import error_dict_objects as object_errors
import pygame

#normal 2d object
class object:
    #variables set by init
    #__position
    #__dimensions

    def __init__(self, position:list[float, float], dimensions:list[float, float]):
        self.__position:list[float, float] = position
        self.__dimensions:list[float, float] = dimensions

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