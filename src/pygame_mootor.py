from error_list import error_dict_standard as std_errors
from error_list import error_dict_events as event_errors
from error_list import error_dict_drawing as draw_errors
from error_list import error_dict_scene as scene_errors
import objects
import pygame

#could implement a modifiable settings list/file

#event handling stuff
def __event_response_undefined(Mootor, event) -> None:
    raise Exception(event_errors[1])

def define_pygame_event(eventName:str, pygameEquivelent, forceOverride:bool = False):
    if eventName in pygame_events.keys() and not forceOverride:
        raise Exception(event_errors[2])
    else:
        if forceOverride:
            print("Overriding event definitions is unadvisable. :/")
        pygame_events[eventName] = pygameEquivelent

def define_event_response(event:str, response) -> None:
    pygame_event_responses[event] = response

pygame_events:dict = {
    "QUIT": pygame.QUIT
}

#every responses first parameter must be the main Mootor class
#second parameter shall be the event itself or rather it's returned value
pygame_event_responses:dict = {
    "QUIT": __event_response_undefined
}

def testFunc(mootor): print("yes is Col")
testTexGroup = objects.textureGroup((255, 0, 0, 255))
#testTexGroup.addTexture("std", "src/textures/heartPixel1.png")
testcase = objects.object(objects.test_base_settings, testTexGroup)
testcase2 = objects.object(objects.test_base_settings2, testTexGroup)

#mootor SHALL DRAW the currently selected SCENE object
#scene object shall contain and manage data relating to objects in a given scene
#and which operations to currently perform on them
class scene:
    #variables set by class
    #__object_list

    #object in list shall take the following format:
    #[objectReference, operationsString]
    #operationsString shall be deconstructed and interpreted during runtime for what
    #object functions to call

    def __init__(self):
        self.__object_list:dict[str:list[list]] = {}

    def addLayer(self, layerName:str, forceOverRide:bool = False):
        if layerName in self.__object_list.keys() and not forceOverRide:
            raise Exception(scene_errors[1])
                
        self.__object_list[layerName] = []

    def getLayerNames(self):
        return self.__object_list.keys()
    
    def addToLayer(self, object:objects.object, operations:str, layerName:str, forceOverRide:bool = False):
        if layerName not in self.getLayerNames():
            raise Exception(scene_errors[2])
        
        if object in self.__object_list[layerName] and not forceOverRide:
            raise Exception(scene_errors[3])
        
        self.__object_list[layerName].append([object, operations])

    def getObjectOperations(self, object:objects.object, layerName:str):
        if layerName not in self.getLayerNames():
            raise Exception(scene_errors[2])
        
        for i in self.__object_list[layerName]:
            if i[0] == object:
                return i[1]
            
        raise Exception(scene_errors[6])

    def modifyObjectOperations(self, object:objects.object, newOperations:str, layerName:str):
        if layerName not in self.getLayerNames():
            raise Exception(scene_errors[2])
        
        for i in self.__object_list[layerName]:
            if i[0] == object:
                #we assume i is a reference to value in the dict
                #pray it works, fuck python otherwise it would be easy
                i[1] = newOperations
                return

        raise Exception(scene_errors[5])

    def removeFromLayer(self, object:objects.object, layerName:str):
        if layerName not in self.getLayerNames():
            raise Exception(scene_errors[2])
        
        for i in self.__object_list[layerName]:
            if i[0] == object:
                self.__object_list[layerName].pop(i)
                return
            
        raise Exception(scene_errors[4])

#põhiline mootori klass
class Mootor:
    #variables set by class
    #__screen
    #__clock
    #__running
    #__handled_events
    #__current_center
    #__interaction_field_size

    #variables set by init
    #__display_size

    #optional variables to be set by function call
    #__use_fps_limit
    #__fps_limit

    #constructor
    def __init__(self, display_size:tuple[int, int]) -> None:
        #start pygame
        if not pygame.get_init():
            pygame.init()
        else:
            raise Exception(std_errors[1])
        
        #set display
        self.__screen = pygame.display.set_mode(display_size)
        self.__display_size = display_size

        #init clock
        #think about another time system implementation
        self.__clock = pygame.time.Clock()

        #handle other
        self.__handeled_events:list[str] = []

        #interaction for in game things (can be overwritten when adding a player object
        #to the Mootor)
        #__current_center is as the name imples the current position of the middle of the screen on the global map
        self.__current_center:list[float, float] = [0, 0] #[self.__display_size[0] / 2, self.__display_size[1] / 2]
        self.__interaction_field_size:list[float, float] = [100, 100]

        #init some optional variables
        self.__use_backround_colour:bool = False
        self.__background_colour:tuple[int, int, int, int] = None

        self.__use_fps_limit:bool = False
        self.__fps_limit:float = None

        #set running
        self.__running = True

    #destructor
    def __del__(self):
        pygame.quit()

    def get_screen(self):
        return self.__screen

    #overall operations
    #is running
    def is_alive(self) -> bool:
        return self.__running
    
    #set running to false
    def kill_program(self) -> None:
        self.__running = False

    #events
    def add_handelable_event(self, event:str) -> None:
        self.__handeled_events.append(event)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            for active_handelable in self.__handeled_events:
                if event.type == pygame_events[active_handelable]:
                    pygame_event_responses[active_handelable](self, event)

    def get_current_center(self):
        return self.__current_center
    
    def get_interaction_field_size(self):
        return self.__interaction_field_size

    #drawing
    def use_background_colour(self, use:bool):
        self.__use_backround_colour = use

    #we could overload to enable values other than rgba
    def set_background_colour(self, colour:tuple[int, int, int, int]):
        self.__background_colour = colour

    def __flip_display(self) -> None:
        pygame.display.flip()

    #draw complete also handles object tied events
    def draw_complete(self):
        #implement proper draw order system and scene system later with proper objects
        if self.__use_backround_colour:
            if self.__background_colour != None:
                self.__screen.fill(self.__background_colour)
            else:
                raise Exception(draw_errors[1])
            
        testcase.draw(self)

        self.__flip_display()

    #time/fps handling
    def use_fps_limit(self, use:bool) -> None:
        self.__use_fps_limit = use

    def set_fps_limit(self, limit:float) -> None:
        if not (limit < 0.01):
            self.__fps_limit = limit
        else:
            raise Exception(std_errors[3])

    def handle_time(self) -> None:
        if self.__use_fps_limit:
            if self.__fps_limit != None:
                self.__clock.tick(self.__fps_limit)
            else:
                raise Exception(std_errors[2])