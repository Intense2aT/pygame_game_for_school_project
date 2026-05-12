import pygame_mootor as mootor
import objects
import pygame

# pygame setup
display_size:tuple[int, int] = (1280, 720)
manager = mootor.Mootor(display_size)

#trust me
def end_exec(Mootor:mootor.Mootor, event):
    Mootor.kill_program()

def on_mouse_motion(Mootor:mootor.Mootor, event):
    Mootor.set_cur_mouse_position(event.__dict__['pos'])

def on_mouse_up(Mootor:mootor.Mootor, event):
    if 0 < event.__dict__['button'] < 4:
        states = Mootor.get_cur_mousebutton_states()
        updated_states = []
        for i in states:
            updated_states.append(i)
        updated_states[event.__dict__['button'] - 1] = False
        
        Mootor.set_cur_mousebutton_states(updated_states)
    else:
        print(f"does not handle mouse button {event.__dict__['button']}")

def on_mouse_down(Mootor:mootor.Mootor, event):
    if 0 < event.__dict__['button'] < 4:
        states = Mootor.get_cur_mousebutton_states()
        updated_states = []
        for i in states:
            updated_states.append(i)
        updated_states[event.__dict__['button'] - 1] = True

        Mootor.set_cur_mousebutton_states(updated_states)
    else:
        print(f"does not handle mouse button {event.__dict__['button']}")

mootor.define_event_response("QUIT", end_exec)
manager.add_handelable_event("QUIT")

mootor.define_event_response("MOUSEMOTION", on_mouse_motion)
manager.add_handelable_event("MOUSEMOTION")

mootor.define_event_response("MOUSEBUTTONUP", on_mouse_up)
manager.add_handelable_event("MOUSEBUTTONUP")

mootor.define_event_response("MOUSEBUTTONDOWN", on_mouse_down)
manager.add_handelable_event("MOUSEBUTTONDOWN")

manager.use_fps_limit(True)
manager.set_fps_limit(30)

manager.use_background_colour(True)
manager.set_background_colour((0, 0, 0, 255))

test_base_settings:list = [
    [1180, 0], #position
    [100, 40], #dimensions   
]

def testFunc1(mootor): pass #mootor.kill_program()
def testFunc1_interact(mootor): mootor.kill_program()
testTexGroup = objects.textureGroup((255, 0, 0, 255))
#testTexGroup.addTexture("std", "src/textures/heartPixel1.png")
testTexGroup.addFont("Tiny5-10", "src/fonts/Tiny5/Tiny5-Regular.ttf", 10)
testcase = objects.object(test_base_settings, testTexGroup)
testcase.set_game_interact_func(testFunc1)
testcase.set_call_on_press(True)
testcase.set_ui_interact_func(testFunc1_interact)

testcase.set_draw_with_text(True)
testcase.set_text_to_draw("Quit")
testcase.set_text_colour([0, 255, 0, 255])
testcase.set_text_dimensions_scale_rel(1, 1)
testcase.update_rendered_text("Tiny5-10")

scene = mootor.scene()
scene.addLayer("layer_1")
scene.addToLayer(testcase, "draw/ui_interact", "layer_1")

manager.set_cur_renderable_scene(scene)

while manager.is_alive():
    #event handling
    manager.handle_events()
    #print(f"{manager.get_cur_mouse_position()} ja {manager.get_cur_mousebutton_states()} ja {manager.get_prev_mousebutton_states()}")

    # RENDER YOUR GAME HERE
    manager.draw_complete()

    manager.handle_time()