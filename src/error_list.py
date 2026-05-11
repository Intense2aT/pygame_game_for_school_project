error_dict_standard:dict = {
    1: "Standard Error 1: Pygame already initialized.",
    2: "Standard Error 2: Using fps limit, but float value of the limit is undefined",
    3: "standard Error 3: Fps limit was set to an impossible / most likely unwanted value.",
}

error_dict_events:dict = {
    1: "Event Handling Error 1: Response to an event is undefined.",
    2: "Event Handling Error 2: Eventname in pygame_events is already defined and forceOverride is false.",
}

error_dict_drawing:dict = {
    1: "Drawing Error 1: Using background colour, but value of background colour is undefined",
    2: "Drawing Error 2: Current rederable scene not set for draw call."
}

error_dict_texture_group:dict = {
    1: "Texture Error 1: adding texture to group but chosen texture name is already bound and overWriteExisting == False.",
    2: "Texture Error 2: texture name used in getTexture() does not exist in textureGroup",
    3: "Texture Error 3: adding font to the group but chosen font name is already bound",
    4: "Texture Error 4: font name used in getFont() does not exist in textureGroup"
}

error_dict_objects:dict = {
    1: "Object Error 1: Adjusting the dimensions of an object resulted in a negative value for object size.",
    2: "Object Error 2: Object draw() argument drawType is not coloured or textured :/",
    3: "Object Error 3: Variable textureName not set for textured draw call.",
    4: "Object Error 4: Type of interaction field set is not \"global\"/\"local\"",
}

error_dict_scene:dict = {
    1: "Scene Error 1: Layer name already in scene, unable to add layer of given name.",
    2: "Scene Error 2: Layer name not in scene",
    3: "Scene Error 3: Object already in layer, unable to add given object to given layer",
    4: "Scene Error 4: Object not in given layer, unable to remove nonexistent object.",
    5: "Scene Error 5: Object not in given layer, unable to modify operations of nonexistent object.",
    6: "Scene Error 6: Object not in given layer. again... :D"
}