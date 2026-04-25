import pygame_mootor as mootor

# pygame setup
display_size:tuple[int, int] = (1280, 720)
manager = mootor.Mootor(display_size)

def end_exec(Mootor:mootor.Mootor):
    Mootor.kill_program()

mootor.define_event_response("QUIT", end_exec)
manager.add_handelable_event("QUIT")

while manager.is_alive():
    #event handling
    manager.handle_events()


    # fill the screen with a color to wipe away anything from last frame
    manager.draw_test()

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    manager.flip_display()

    #clock.tick(60)  # limits FPS to 60