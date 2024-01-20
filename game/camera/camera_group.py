import pyscroll 

class CameraGroup(pyscroll.PyscrollGroup):
    def __init__(self, map_layer):
        super().__init__(map_layer = map_layer, default_layer = 1)
    
    def check_flipped(self):
        print("asdf")