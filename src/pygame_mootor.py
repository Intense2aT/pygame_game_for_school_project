from error_list import error_dict_standard as std_errors
from error_list import error_dict_events as event_errors
import pygame

#could implement a modifiable settings list/file

#event handling stuff
def __event_response_undefined(Mootor) -> None:
    raise Exception(event_errors[1])

def define_event_response(event:str, response) -> None:
    pygame_event_responses[event] = response

pygame_events:dict = {
    "QUIT": pygame.QUIT
}

#every responses first parameter must be the main Mootor class
pygame_event_responses:dict = {
    "QUIT": __event_response_undefined
}

#põhiline mootori klass
class Mootor:
    #variables set by class
    #__screen
    #__clock
    #__running
    #__handled_events

    #variables set by init
    #__display_size

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

        #set running
        self.__running = True

    #destructor
    def __del__(self):
        #closing pygame
        pygame.quit()

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
                    pygame_event_responses[active_handelable](self)

    #drawing
    def draw_test(self):
        self.__screen.fill("purple")

    def flip_display(self) -> None:
        pygame.display.flip()
