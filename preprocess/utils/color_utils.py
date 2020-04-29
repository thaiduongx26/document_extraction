def generate_random_bright_color():
    import random
    import colorsys
    h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
    r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]

    return "#%02X%02X%02X" % (r, g, b)
