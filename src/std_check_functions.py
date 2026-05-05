import os
import pygame

#we check if any of the 4 corners of object 2 are in the first object, confirming collision
#when object is taken from the center, we assume the given dimensions are the diameter not the radius
def collision_two_rectangles_no_rotation(object1:list[list[float, float], list[float, float]],
                                         object2:list[list[float, float], list[float, float]],
                                         object1FromTopLeft:bool = False,
                                         object2FromTopLeft:bool = False) -> bool:
    
    object1Points:list[list, list, list, list] = []
    if object1FromTopLeft:
        object1Points.append(object1[0])
        object1Points.append([object1[0][0] + object1[1][0], object1[0][1]])
        object1Points.append([object1[0][0], object1[0][1] + object1[1][1]])
        object1Points.append([object1[0][0] + object1[1][0], object1[0][1] + object1[1][1]])
    else:
        object1Points.append([object1[0][0] - 0.5 * object1[1][0], object1[0][1] - 0.5 * object1[1][1]])
        object1Points.append([object1[0][0] + 0.5 * object1[1][0], object1[0][1] - 0.5 * object1[1][1]])
        object1Points.append([object1[0][0] - 0.5 * object1[1][0], object1[0][1] + 0.5 * object1[1][1]])
        object1Points.append([object1[0][0] + 0.5 * object1[1][0], object1[0][1] + 0.5 * object1[1][1]])

    object2Points:list[list, list, list, list] = []
    if object2FromTopLeft:
        object2Points.append(object2[0])
        object2Points.append([object2[0][0] + object2[1][0], object2[0][1]])
        object2Points.append([object2[0][0], object2[0][1] + object2[1][1]])
        object2Points.append([object2[0][0] + object2[1][0], object2[0][1] + object2[1][1]])
    else:
        object2Points.append([object2[0][0] - 0.5 * object2[1][0], object2[0][1] - 0.5 * object2[1][1]])
        object2Points.append([object2[0][0] + 0.5 * object2[1][0], object2[0][1] - 0.5 * object2[1][1]])
        object2Points.append([object2[0][0] - 0.5 * object2[1][0], object2[0][1] + 0.5 * object2[1][1]])
        object2Points.append([object2[0][0] + 0.5 * object2[1][0], object2[0][1] + 0.5 * object2[1][1]])

    for point in object2Points:
        if object1Points[0][0] < point[0] and object1Points[3][0] > point[0] and object1Points[0][1] < point[1] and object1Points[3][1] > point[1]:
            return True
    
    for point in object1Points:
        if object2Points[0][0] < point[0] and object2Points[3][0] > point[0] and object2Points[0][1] < point[1] and object2Points[3][1] > point[1]:
            return True
        
    return False