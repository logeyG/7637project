from PIL import Image
from PIL import ImageChops
import math
from visual import utility


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


def find_regions(figure):

    # solution modified from this StackOverflow answer:
    # http://stackoverflow.com/questions/1989987/my-own-ocr-program-in-python
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

def intersect(source, compare):

    pixels_to_remove = []

    width, height = compare.size
    compare_pixels = compare.load()
    for x in range(width):
        for y in range(height):
            # look for a black pixel
            if compare_pixels[x, y] == (0, 0, 0, 255):  # black pixel
                pixels_to_remove.append((x, y))

    width, height = source.size
    source_pixels = source.load()
    for x in range(width):
        for y in range(height):

            # fuzzy remove
            if (x, y) in pixels_to_remove:
                source_pixels[x, y] = (255, 255, 255, 255)

                source_pixels[x + 1, y] = (255, 255, 255, 255)
                source_pixels[x, y + 1] = (255, 255, 255, 255)
                source_pixels[x - 1, y] = (255, 255, 255, 255)
                source_pixels[x, y - 1] = (255, 255, 255, 255)

                source_pixels[x + 2, y] = (255, 255, 255, 255)
                source_pixels[x, y + 2] = (255, 255, 255, 255)
                source_pixels[x - 2, y] = (255, 255, 255, 255)
                source_pixels[x, y - 2] = (255, 255, 255, 255)

    return source


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
