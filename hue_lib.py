from phue import Bridge
from rgbxy import ColorHelper, Converter
from autoyaml import load_config, write_config
from random import randint
from time import sleep

CONFIG = load_config('dancing_lights')
BRIDGE = Bridge(CONFIG.get('ip'))
HELPER = ColorHelper()
CONVERTER = Converter()

def get_lights():
    return BRIDGE.get_light_objects()

def get_xy(r, g, b):
    r = int(r)
    g = int(g)
    b = int(b)
    return CONVERTER.rgb_to_xy(r, g, b)

def get_rgb(x,y,br):
    return HELPER.get_rgb_from_xy_and_brightness(x, y, br)

def set_color(light, r, g, b):
    xy = get_xy(r, g, b)
    light.xy = xy


def set_all_color(r, g, b):
    for l in get_lights():
        set_color(l, r, g, b)

def random_colors():
    bag =  set()
    for i in range(3):
        bag.add(randint(0, 50 * (i+1)))
    colors = [ i for i in bag ]
    if len(colors) < 2:
        colors.append(randint(0,255))
    if len(colors) < 3:
        colors.append(randint(0,255))
    return colors


def disco():
   while True:
      for l in get_lights():
         colors = random_colors()
         set_color(l, *colors)

if __name__ == "__main__":
    #disco()
    pass
