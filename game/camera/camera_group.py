import pyscroll 

class CameraGroup(pyscroll.PyscrollGroup):
    def __init__(self, map_layer, default_layer):
        super().__init__(map_layer = map_layer, default_layer = default_layer)