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
}

error_dict_texture_group:dict = {
    1: "Texture Error 1: adding texture to group but chosen texture name is already bound and overWriteExisting == False.",
    2: "Texture Error 2: texture name used in getTexture() does not exist in textureGroup",
}

error_dict_objects:dict = {
    1: "Object Error 1: Adjusting the dimensions of an object resulted in a negative value for object size.",
    2: "Object Error 2: Object draw() argument drawType is not coloured or textured :/",
    3: "Object Error 3: Variable textureName not set for textured draw call.",
}