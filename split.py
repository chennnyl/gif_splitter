from PIL import Image, ImageSequence
from sys import argv, exit
from os import mkdir

import logging
logging.basicConfig(format="%(levelname)s: %(message)s")

argv = argv[1:]

try:
    filename = argv[0].split("/")[-1]
except IndexError:
    logging.error("No filename supplied")
    exit()

try:
    columns, rows = [float(a) for a in argv[1:]]
except:
    logging.info("Bad (or no) ratio given; defaulting to 5x3")
    columns, rows = (5, 3)

im = Image.open(argv[0])

folder_name = "".join(filename.split(".")[:-1])

example = (50, 50)

try:
    mkdir(folder_name)
except:
    pass

col_size = im.size[0] / columns
row_size = im.size[1] / rows

cells = [[None, (i%columns, i//columns)] for i in range(columns*rows)]

imit = ImageSequence.Iterator(im)

for i,cell in enumerate(cells):
    x,y = cell[1]

    cells[i][0] = []

    for frame in range(im.n_frames):

        cells[i][0].append( imit[frame].crop((col_size*x, row_size*y, col_size*(x+1), row_size*(y+1))) )

    if len(cells[i][0]) == 1:
        logging.warn("Only found 1 image; saving anyway")
        cells[i][0][0].save("out/" + folder_name + "/" + folder_name + str(cell[1]) + ".gif")
    else:
        cells[i][0][0].save("out/" + folder_name + "/" + folder_name + str(cell[1]) + ".gif", save_all = True, duration = 100, append_images = cells[i][0][1:])

    logging.info(f"Finished frame {i}")