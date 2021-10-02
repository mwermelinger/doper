"""
raster.py – read/write a raster image (matrix of RGB pixels) from/to a file
"""

import matplotlib.pyplot as plt
import PIL
from typing import List

RGB = List[int]                     # list of 3 integers
Raster = List[List[RGB]]            # matrix of RGB triples

R = 0                               # red, green, blue indices in a pixel
G = 1
B = 2

WHITE   = [255, 255, 255]           # the 16 standard web colours
SILVER  = [192, 192, 192]
GRAY    = [128, 128, 128]
BLACK   = [  0,   0,   0]
RED     = [255,   0,   0]
MAROON  = [128,   0,   0]
YELLOW  = [255, 255,   0]
OLIVE   = [128, 128,   0]
LIME    = [  0, 255,   0]
GREEN   = [  0, 128,   0]
ACQUA   = [  0, 255, 255]
TEAL    = [  0, 128, 128]
BLUE    = [  0,   0, 255]
NAVY    = [  0,   0, 128]
FUCHSIA = [255,   0, 255]
PURPLE  = [128,   0, 128]


def load(filename: str) -> Raster:
    """Load the given file and return the image.

    The file must exist and be in any of the formats read by PIL:
    https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html

    The returned image is a matrix of pixels.
    The matrix is a list of rows, from the image's top to bottom,
    with each row a list of pixels, from left to right.
    All rows have the same length.
    Each pixel is a list of three integers from 0 to 255 (inclusive),
    representing the red-green-blue components of the pixel.
    """
    image = PIL.Image.open(filename)
    if image.mode not in ('RGBA', 'RGB', 'L', '1'):
        raise ValueError('image cannot be converted to RGB format')
    pixels = []
    for row in range(image.height):
        row_pixels = []
        for column in range(image.width):
            pixel = image.getpixel((column, row))   # integer or tuple
            if image.mode == 'RGB':
                pixel = list(pixel)
            elif image.mode == 'RGBA':      # RGB + alpha channel:
                pixel = list(pixel[:3])         # ignore transparency
            elif image.mode == 'L':         # greyscale image:
                pixel = [pixel] * 3             # set same R, G, B values
            else:                           # B&W image: zeros and ones
                pixel = [255 * pixel] * 3
            row_pixels.append(pixel)
        pixels.append(row_pixels)
    return pixels


def save(image: Raster, filename: str) -> None:
    """Save the image to the given file, overwriting it if it exists.

    The filename must have an extension to indicate the file format,
    which must be a format written by PIL:
    https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
    """
    img = PIL.Image.new('RGB', (width(image), height(image)))
    for column in range(width(image)):
        for row in range(height(image)):
            img.putpixel((column, row), tuple(image[row][column]))
    img.save(filename)


def width(image: Raster) -> int:
    """Return how many columns of pixels the image has."""
    return len(image[0]) if image else 0


def height(image: Raster) -> int:
    """Return how many rows of pixels the image has."""
    return len(image)


def show(image: Raster) -> None:
    """Show the image, resized to not be too large or small."""
    plt.axis('off')         # don't show the x and y axes
    plt.imshow(image)
