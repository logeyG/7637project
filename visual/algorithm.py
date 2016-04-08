from PIL import Image
from PIL import ImageChops
from visual import utility
from operator import itemgetter
import math
import numpy



class Region():
    # solution modified from this StackOverflow answer:
    # http://stackoverflow.com/questions/1989987/my-own-ocr-program-in-python
    def __init__(self, x, y):
        self._pixels = [(x, y)]
        self._min_x = x
        self._max_x = x
        self._min_y = y
        self._max_y = y

    def add(self, x, y):
        self._pixels.append((x, y))
        self._min_x = min(self._min_x, x)
        self._max_x = max(self._max_x, x)
        self._min_y = min(self._min_y, y)
        self._max_y = max(self._max_y, y)

    def box(self):
        return [(self._min_x, self._min_y), (self._max_x, self._max_y)]

def find_first_edge(figure):

    img = Image.open(figure.visualFilename)
    pixels = img.load()

    width, height = img.size
    pixels = img.load()
    for x in range(width):
        for y in range(height):
            # look for a black pixel
            if pixels[x, y] == (0, 0, 0, 255):  # black pixel
                return (x, y)

    return (0, 0)


def find_image_size(figure):

    img = Image.open(figure.visualFilename)
    pixels = img.load()
    width, height = img.size
    pixels = img.load()

    black_pixels = []
    for x in range(width):
        for y in range(height):
            # look for a black pixel
            if pixels[x, y] == (0, 0, 0, 255):  # black pixel
                black_pixels.append((x, y))

    x_black = min(black_pixels, key=itemgetter(1))[1], max(black_pixels, key=itemgetter(1))[1]
    y_black = min(black_pixels)[0], max(black_pixels)[0]

    b_width = x_black[1] - x_black[0]
    b_height = y_black[1] - y_black[0]

    return b_width * b_height

def get_center(blobs):

    closest = []

    for blob in blobs:
        nodes = utility.convert_to_easy_array(blob.load())
        closest.append(nodes[utility.closest_node((92, 92), nodes)])

    return utility.closest_node((92, 92), closest)

def write_blobs(blobs):

    outer_shapes = Image.new("RGBA", (184, 184), "white")
    outer_pixels = outer_shapes.load()

    for blob in blobs:
        pixels = blob.load()
         # first pass. find regions.
        for x in range(184):
            for y in range(184):
            # look for a black pixel
                if pixels[x, y] == (0, 0, 0, 255):  # black pixel
                    outer_pixels[x, y] = (0, 0, 0, 255)

    return outer_shapes

def find_regions(figure):

    # solution modified from this StackOverflow answer:
    # http://stackoverflow.com/questions/1989987/my-own-ocr-program-in-python

    if isinstance(figure, dict):
        img = Image.open(figure['visualFilename'])
    else:
        img = Image.open(figure.visualFilename)
    pixels = img.load()

    width, height = img.size
    pixels = img.load()
    regions = {}
    pixel_region = [[0 for y in range(height)] for x in range(width)]
    equivalences = {}
    n_regions = 0

    # first pass. find regions.
    for x in range(width):
        for y in range(height):
            # look for a black pixel
            if pixels[x, y] == (0, 0, 0, 255):  # black pixel
                # get the region number from north or west
                # or create new region
                region_n = pixel_region[x - 1][y] if x > 0 else 0
                region_w = pixel_region[x][y - 1] if y > 0 else 0

                max_region = max(region_n, region_w)

                if max_region > 0:
                    # a neighbour already has a region
                    # new region is the smallest > 0
                    new_region = min(filter(lambda i: i > 0, (region_n, region_w)))
                    # update equivalences
                    if max_region > new_region:
                        if max_region in equivalences:
                            equivalences[max_region].add(new_region)
                        else:
                            equivalences[max_region] = set((new_region, ))
                else:
                    n_regions += 1
                    new_region = n_regions

                pixel_region[x][y] = new_region

    # scan image again, assigning all equivalent regions the same region value
    for x in range(width):
        for y in range(height):
            r = pixel_region[x][y]
            if r > 0:
                while r in equivalences:
                    r = min(equivalences[r])

                if not r in regions:
                    regions[r] = Region(x, y)
                else:
                    regions[r].add(x, y)

    return list(regions.items())

def get_blobs(regions):

    blobs = []
    for region in regions:

        pixels = region[1]._pixels
        blob = Image.new("RGBA", (184, 184), "white")

        blob_pixels = blob.load()
        for p in pixels:
            blob_pixels[p[0], p[1]] = (0, 0, 0, 255)

        blobs.append(blob)

    return blobs


def ncc(im1, im2):

    n = 33856
    image, template = utility.open_image(im1, im2)

    np_image = numpy.asarray(image.getdata())
    np_template = numpy.asarray(template.getdata())

    image_mean = np_image.mean()
    image_std = np_image.std()

    template_mean = np_template.mean()
    template_std = np_template.std()

    s = sum(  ( image_mean / image_std ) * ( template_mean / template_std)  )
    x = 1 / n * s

    return x

def calc_rms(im1, im2):

    # http://effbot.org/zone/pil-comparing-images.htm#rms
    # calculate the root-mean-square difference between two images
    source, compare = utility.open_image(im1, im2)

    "Calculate the root-mean-square difference between two images"
    diff = ImageChops.difference(source, compare)
    h = diff.histogram()
    sq = (value * (idx**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(source.size[0] * source.size[1]))
    return round(rms, 0)


def image_difference(im1, im2):

    source, compare = utility.open_image(im1, im2)
    return ImageChops.difference(source, compare).getbbox()

def subtract(source, compare):

    compare_pixels = compare.load()
    width, height = source.size
    source_pixels = source.load()

    for x in range(width):
        for y in range(height):
            # fuzzy remove
            if compare_pixels[x, y] == (0, 0, 0, 255):

                source_pixels[x, y] = (255, 255, 255, 255)
                source_pixels[x + 1, y] = (255, 255, 255, 255)
                source_pixels[x, y + 1] = (255, 255, 255, 255)
                source_pixels[x - 1, y] = (255, 255, 255, 255)
                source_pixels[x, y - 1] = (255, 255, 255, 255)

    return source

def intersect(source, compare):

    width, height = 184, 184
    compare_pixels = compare.load()
    source_pixels = source.load()

    intersect_image = Image.new("RGBA", (width, height), "white")
    intersect_pixels = intersect_image.load()

    for x in range(width):
        for y in range(height):
            # fuzzy remove
            if compare_pixels[x, y] == (0, 0, 0, 255) and source_pixels[x, y] == (0, 0, 0, 255):
                intersect_pixels[x, y] = (0, 0, 0, 255)

    return intersect_image

def modified_subtract(source, compare, orientation):

    width, height = 184, 184
    compare_pixels = compare.load()
    source_pixels = source.load()

    for x in range(width):
        for y in range(height):
            # fuzzy remove
            if compare_pixels[x, y] == (0, 0, 0, 255):
                if orientation == 'horizontal':
                    if x >= 51:
                        source_pixels[x - 51, y] = (255, 255, 255, 255)
                elif orientation == 'vertical':
                    if y < (184 - 51):
                        source_pixels[x, y + 51] = (255, 255, 255, 255)

    mod_image = Image.new("RGBA", (width, height), "white")
    mod_pixels = mod_image.load()

    for x in range(width):
        for y in range(height):
            if source_pixels[x, y] == (0, 0, 0, 255):
                if orientation == 'horizontal':
                    if x >= 20:
                        mod_pixels[x - 20, y] = (0, 0, 0, 255)
                elif orientation == 'vertical':
                    if y < (184 - 20):
                        mod_pixels[x, y + 20] = (0, 0, 0, 255)

    #source.show()
    return mod_image

def xor(source, compare):

    width, height = source.size

    source_pixels = source.load()
    compare_pixels = compare.load()

    xor_image = Image.new("RGBA", (width, height), "white")
    xor_pixels = xor_image.load()

    for x in range(width):
        for y in range(height):
            if (source_pixels[x, y] == (0, 0, 0, 255) and compare_pixels[x, y] != (0, 0, 0, 255)
                or source_pixels[x, y] != (0, 0, 0, 255) and compare_pixels[x, y] == (0, 0, 0, 255)):
                xor_pixels[x, y] = (0, 0, 0, 255)

    return xor_image

def fill_ratio(figure):

    if hasattr(figure, 'visualFilename'):
        img = Image.open(figure.visualFilename)
    else:
        img = figure

    filled_pixels = 0
    pixels = img.load()

    width, height = img.size
    pixels = img.load()
    for x in range(width):
        for y in range(height):
            # look for a black pixel
            if pixels[x, y] == (0, 0, 0, 255):  # black pixel
                filled_pixels += 1

    return filled_pixels

def get_sizes(size_in, rows, columns):

    # https://www.reddit.com/r/learnpython/comments/2jlv1e/
    # python_script_to_take_an_image_and_cut_it_into_4/
    width, height = size_in
    new_width = width / columns
    new_height = height / rows
    sizes_out = []
    for x in range(columns):
        for y in range(rows):
            sizes_out.append((
                math.floor(x * new_width),
                math.floor(y * new_height),
                math.floor(x * new_width + new_width),
                math.floor(y * new_height + new_height)))
    return sizes_out

def get_sections(figure, size_in, rows, columns):

    image = Image.open(figure.visualFilename)
    sizes = get_sizes(size_in, rows, columns)
    image_sections = []
    for i, size in enumerate(sizes):
        image_sections.append(image.crop(size))

    return image_sections

def reflected_within(H1, H2):

    H1__A_sections = get_sections(H1[0], (184, 184), 1, 2)
    H1__C_sections = get_sections(H1[1], (184, 184), 1, 2)

    H2__D_sections = get_sections(H2[0], (184, 184), 1, 2)
    H2__F_sections = get_sections(H2[1], (184, 184), 1, 2)

    return (calc_rms(H1__A_sections[0].transpose(Image.FLIP_LEFT_RIGHT), H1__A_sections[1]) <= 962.0,
            calc_rms(H1__C_sections[0].transpose(Image.FLIP_LEFT_RIGHT), H1__C_sections[1]) <= 958.0,
            calc_rms(H2__D_sections[0].transpose(Image.FLIP_LEFT_RIGHT), H2__D_sections[1]) <= 962.0,
            calc_rms(H2__F_sections[0].transpose(Image.FLIP_LEFT_RIGHT), H2__F_sections[1]) <= 958.0)

def reflected_within_single(H1, H2):

    H1__A_sections = get_sections(H1, (184, 184), 1, 2)
    H1__C_sections = get_sections(H2, (184, 184), 1, 2)

    return (calc_rms(H1__A_sections[0].transpose(Image.FLIP_LEFT_RIGHT), H1__A_sections[1]) < 965,
            calc_rms(H1__C_sections[0].transpose(Image.FLIP_LEFT_RIGHT), H1__C_sections[1]) < 965)
