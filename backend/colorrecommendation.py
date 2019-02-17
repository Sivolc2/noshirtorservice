def get_complementary(color):

    color = color[1:]

    color = int(color, 16)

    comp_color = 0xFFFFFF ^ color

    comp_color = "#%06X" % comp_color

    return comp_color

def get_monochromatic(color):

    color = color[1:]

    color = int(color, 16)

    sim_color = 0x444444 ^ color

    sim_color1 = 0x333333 ^ sim_color

    sim_color = "#%06x" % sim_color

    sim_color1 = "#%06x" % sim_color1

    return sim_color, sim_color1

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def closest_color(color):

    inputColorArray = ["#008000","#0000FF","#E6E6E6","#923232"] #in hex
    cost = 0
    index = 0
    color = hex_to_rgb(color)
    for input in inputColorArray:
        input = hex_to_rgb(input)
        if cost < (((input[0] - color[0])+(input[1] - color[1])+(input[2] - color[2]))/3) ** 2 :
            cost = (((input[0] - color[0])+(input[1] - color[1])+(input[2] - color[2]))/3) ** 2
            input = rgb_to_hex(input)
            index = inputColorArray.index(input)

    return inputColorArray[index]
def closest_color(color):

    inputColorArray = [] #in hex
    cost = 0
    index = 0
    for input in inputColorArray
        if cost < (input - color) ** 2
            cost = (input - color) ** 2
            index = inputColorArray.index(input)

    return inputColorArray[index]
