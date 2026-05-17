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
manager.set_fps_limit(120)

manager.use_background_colour(True)
manager.set_background_colour((0, 0, 0, 255))

test_base_settings:list = [
    [1080, 0], #position
    [200, 80], #dimensions   
]

def testFunc1(mootor): pass #mootor.kill_program()
def testFunc1_interact(mootor):
    mootor.set_cur_renderable_scene(scene2)
    print("scene 1 button pressed - going to scene 2")
testTexGroup = objects.textureGroup()
testTexGroup.load_from_json("src/game_data/tex_group_1.json")
testcase = objects.object(test_base_settings, testTexGroup)
testcase.load_from_json("src/game_data/object_1.json")
testcase.set_ui_interact_func(testFunc1_interact)
testcase.set_text_dimensions_scale_rel(0.7, 0.7)
testcase.update_rendered_text("Tiny5-10")
testcase.center_text()

scene1 = mootor.scene()
scene1.addLayer("layer_0")
scene1.addToLayer(testcase, "draw/ui_interact", "layer_0")

def testFunc2_interact(mootor): 
    mootor.set_cur_renderable_scene(scene1)
    print("scene 2 button pressed - going to scene 1")
testcase1 = objects.object(test_base_settings, testTexGroup)
testcase1.load_from_json("src/game_data/object_2.json")
testcase1.set_game_interact_func(testFunc1)
testcase1.set_ui_interact_func(testFunc2_interact)
testcase1.set_text_dimensions_scale_rel(0.7, 0.7)
testcase1.update_rendered_text("Tiny5-10")
testcase1.center_text()

scene2 = mootor.scene()
scene2.addLayer("layer_1")
scene2.addLayer("layer_2")
scene2.addToLayer(testcase1, "draw/ui_interact", "layer_1")

test_grid_settings = [
    [-10, -10], #position
    [100, 100], #dimensions   
]
testgrid = objects.object(test_grid_settings, testTexGroup)
testgrid.set_draw_type("textured")
testgrid.set_texture_name("button_1")
testgrid.set_grid_draw(True)
testgrid.set_grid_dimensions([100, 100])

scene2.addToLayer(testgrid, "draw", "layer_2")

manager.set_cur_renderable_scene(scene1)

while manager.is_alive():
    #event handling
    manager.handle_events()
    #print(f"{manager.get_cur_mouse_position()} ja {manager.get_cur_mousebutton_states()} ja {manager.get_prev_mousebutton_states()}")

    # RENDER YOUR GAME HERE
    manager.draw_complete()

    manager.handle_time()