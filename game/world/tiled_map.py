import pytmx 

from config.config import Config

cfg = Config()

class TiledMap:
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth * cfg.SCALE
        self.height = self.tmx_data.height * self.tmx_data.tileheight * cfg.SCALE
        self.total_tiles = self.tmx_data.width * self.tmx_data.height * cfg.SCALE
        #self.tile_coords_dict = {}

    def render(self, screen):
        layer_count = 0
        for layer in self.tmx_data.layers:
            for column in range(self.tmx_data.width):
                for row in range(self.tmx_data.height):
                    image = self.tmx_data.get_tile_image(column, row, layer_count)
                    if image is not None:
                        x_coord = cfg.TILE_SIZE * column 
                        y_coord = cfg.TILE_SIZE * row
                        screen.blit(image, (x_coord, y_coord))
            layer_count = layer_count + 1