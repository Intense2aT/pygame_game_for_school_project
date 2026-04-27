import pygame_mootor as mootor

# pygame setup
display_size:tuple[int, int] = (1280, 720)
manager = mootor.Mootor(display_size)

def end_exec(Mootor:mootor.Mootor):
    Mootor.kill_program()

mootor.define_event_response("QUIT", end_exec)
manager.add_handelable_event("QUIT")

manager.use_fps_limit(True)
manager.set_fps_limit(60)

manager.use_background_colour(True)
manager.set_background_colour((128, 0, 128, 255))

while manager.is_alive():
    #event handling
    manager.handle_events()

    # RENDER YOUR GAME HERE
    manager.draw_complete()

    manager.handle_time()