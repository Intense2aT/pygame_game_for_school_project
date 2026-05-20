import pygame_mootor as mootor
import objects
import pygame

# pygame setup
display_size:tuple[int, int] = (1280, 720)
manager = mootor.Mootor(display_size)

def h_down(Mootor:mootor.Mootor):
    print("h pressed")
def h_up(Mootor:mootor.Mootor):
    print("h released")

manager.add_function_keydown("h", h_down)
manager.add_function_keyup("h", h_up)

#trust me
def end_exec(Mootor:mootor.Mootor, event):
    Mootor.kill_program()

def on_key_down(Mootor:mootor.Mootor, event):
    Mootor.get_keydown_responses()[Mootor.get_keyboard_map()[event.__dict__['key']]](Mootor)

def on_key_up(Mootor:mootor.Mootor, event):
    Mootor.get_keyup_responses()[Mootor.get_keyboard_map()[event.__dict__['key']]](Mootor)

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

mootor.define_event_response("KEYDOWN", on_key_down)
manager.add_handelable_event("KEYDOWN")

mootor.define_event_response("KEYUP", on_key_up)
manager.add_handelable_event("KEYUP")

mootor.define_event_response("MOUSEMOTION", on_mouse_motion)
manager.add_handelable_event("MOUSEMOTION")

mootor.define_event_response("MOUSEBUTTONUP", on_mouse_up)
manager.add_handelable_event("MOUSEBUTTONUP")

mootor.define_event_response("MOUSEBUTTONDOWN", on_mouse_down)
manager.add_handelable_event("MOUSEBUTTONDOWN")

manager.use_fps_limit(False)
manager.set_fps_limit(120)

manager.use_background_colour(True)
manager.set_background_colour((0, 0, 0, 255))

zero_base:list = [
    [0, 0],
    [0, 0]
]

tex_group_floors = objects.textureGroup()
tex_group_floors.load_from_json("game_data/tex_group_floors.json")

tex_group_var = objects.textureGroup()
tex_group_var.load_from_json("game_data/tex_group_var.json")

#main menu init start
def main_menu_button_1_interact(mootor):
    mootor.set_cur_renderable_scene(scene2)
    print("scene 1 button pressed - going to scene 2")
main_menu_button_1 = objects.object(zero_base, tex_group_var)
main_menu_button_1.load_from_json("game_data/main_menu/start_menu_button_START.json")
main_menu_button_1.set_ui_interact_func(main_menu_button_1_interact)
main_menu_button_1.set_texture_size_fix([[3, 6], [2, 4]])
main_menu_button_1.set_interaction_field_for_grid()
main_menu_button_1.fix_interaction_field_to_texture(16)
main_menu_button_1.set_text_dimensions_scale_rel(2.4, 0.7)
main_menu_button_1.update_rendered_text("Tiny5-20")
main_menu_button_1.center_text()
main_menu_button_1.add_differentiated_grid_point("1/1", "nupp_vaike_vasak")
main_menu_button_1.add_differentiated_grid_point("3/1", "nupp_vaike_parem")
main_menu_button_1.prerender_grid(use_redefined_points=True)

def main_menu_button_2_interact(mootor):
    mootor.kill_program()
main_menu_button_2 = objects.object(zero_base, tex_group_var)
main_menu_button_2.load_from_json("game_data/main_menu/start_menu_button_QUIT.json")
main_menu_button_2.set_ui_interact_func(main_menu_button_2_interact)
main_menu_button_2.set_texture_size_fix([[3, 6], [2, 4]])
main_menu_button_2.set_interaction_field_for_grid()
main_menu_button_2.fix_interaction_field_to_texture(16)
main_menu_button_2.set_text_dimensions_scale_rel(1.5, 0.7)
main_menu_button_2.update_rendered_text("Tiny5-20")
main_menu_button_2.center_text()
main_menu_button_2.add_differentiated_grid_point("1/1", "nupp_vaike_vasak")
main_menu_button_2.prerender_grid(use_redefined_points=True)

def main_menu_button_3_interact(mootor):
    print("Settings menu not implemented")
main_menu_button_3 = objects.object(zero_base, tex_group_var)
main_menu_button_3.load_from_json("game_data/main_menu/start_menu_button_SETTINGS.json")
main_menu_button_3.set_ui_interact_func(main_menu_button_3_interact)
main_menu_button_3.set_texture_size_fix([[3, 6], [2, 4]])
main_menu_button_3.set_interaction_field_for_grid()
main_menu_button_3.fix_interaction_field_to_texture(16)
main_menu_button_3.set_text_dimensions_scale_rel(1.5, 0.7)
main_menu_button_3.update_rendered_text("Tiny5-20")
main_menu_button_3.center_text()
main_menu_button_3.add_differentiated_grid_point("1/1", "nupp_vaike_vasak")
main_menu_button_3.prerender_grid(use_redefined_points=True)

background_grid = objects.object(zero_base, tex_group_floors)
background_grid.load_from_json("game_data/main_menu/start_menu_background_grid.json")
background_grid.prerender_grid()

main_menu = mootor.scene()
main_menu.addLayer("layer_0")
main_menu.addLayer("background")
main_menu.addToLayer(main_menu_button_1, "draw/ui_interact", "layer_0")
main_menu.addToLayer(main_menu_button_2, "draw/ui_interact", "layer_0")
main_menu.addToLayer(main_menu_button_3, "draw/ui_interact", "layer_0")
main_menu.addToLayer(background_grid , "draw", "background")
#main menu init end

#scene 2 init start
def testFunc2_interact(mootor): 
    mootor.set_cur_renderable_scene(main_menu)
    print("scene 2 button pressed - going to scene 1")
testcase1 = objects.object(zero_base, tex_group_var)
testcase1.load_from_json("game_data/object_2.json")
testcase1.set_ui_interact_func(testFunc2_interact)
testcase1.set_text_dimensions_scale_rel(0.7, 0.7)
testcase1.update_rendered_text("Tiny5-20")
testcase1.center_text()

scene2 = mootor.scene()
scene2.addLayer("layer_1")
scene2.addToLayer(testcase1, "draw/ui_interact", "layer_1")
#scene 2 init end

manager.set_cur_renderable_scene(main_menu)

while manager.is_alive():
    #event handling
    manager.handle_events()
    #print(f"{manager.get_cur_mouse_position()} ja {manager.get_cur_mousebutton_states()} ja {manager.get_prev_mousebutton_states()}")

    # RENDER YOUR GAME HERE
    manager.draw_complete()

    manager.handle_time()