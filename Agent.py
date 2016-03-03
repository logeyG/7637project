# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

import math
import operator
# Install Pillow and uncomment this line to access image processing.
from PIL import Image
from PIL import ImageChops
from functools import reduce


class Region():
    # solution modified from this stackoverflow answer:
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


def setup(problem, figures, solutions):

    print('solving problem ' + problem.name)
    if problem.problemType == '3x3':
        a = problem.figures["A"]
        b = problem.figures["B"]
        c = problem.figures["C"]
        d = problem.figures["D"]
        e = problem.figures["E"]
        f = problem.figures["F"]
        g = problem.figures["G"]
        h = problem.figures["H"]

        _1 = problem.figures["1"]
        _2 = problem.figures["2"]
        _3 = problem.figures["3"]
        _4 = problem.figures["4"]
        _5 = problem.figures["5"]
        _6 = problem.figures["6"]
        _7 = problem.figures["7"]
        _8 = problem.figures["8"]

        figures = [a, b, c, d, e, f, g, h]
        solutions = [_1, _2, _3, _4, _5, _6, _7, _8]
    else:
        a = problem.figures["A"]
        b = problem.figures["B"]
        c = problem.figures["C"]

        _1 = problem.figures["1"]
        _2 = problem.figures["2"]
        _3 = problem.figures["3"]
        _4 = problem.figures["4"]
        _5 = problem.figures["5"]
        _6 = problem.figures["6"]

        figures = [a, b, c]
        solutions = [_1, _2, _3, _4, _5, _6]


def find_regions(figure):
    # solution modified from this stackoverflow answer:
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


def equality(source, compare):

    if hasattr(source, 'visualFilename'):
        source = Image.open(source.visualFilename)
        compare = Image.open(compare.visualFilename)

    # http://effbot.org/zone/pil-comparing-images.htm#rms
    # calculate the root-mean-square difference between two images
    h = ImageChops.difference(source, compare).histogram()
    # calculate rms
    equality = math.sqrt(reduce(operator.add,
                                map(lambda h, i: h * (i**2), h, range(256))
                                ) / (float(source.size[0]) * source.size[1]))
    if equality < 0.1:
        return True
    else:
        return False


def shape_delta(source, compare):
    source_count = len(find_regions(source))
    compare_count = len(find_regions(compare))

    if source_count < compare_count:
        return 'added_' + str(compare_count - source_count)
    elif source_count > compare_count:
        return 'removed_' + str(source_count - compare_count)
    else:
        return 'unchanged'


def h_flip(figure1, figure2):
    source = Image.open(figure1.visualFilename)
    flipped = Image.open(figure2.visualFilename).transpose(Image.FLIP_LEFT_RIGHT)
    return equality(source, flipped)


def v_flip(figure1, figure2):
    source = Image.open(figure1.visualFilename)
    flipped = Image.open(figure2.visualFilename).transpose(Image.FLIP_TOP_BOTTOM)
    return equality(source, flipped)


def rotation(figure1, figure2):
    source = Image.open(figure1.visualFilename)
    rotate90 = Image.open(figure2.visualFilename).transpose(Image.ROTATE_90)
    rotate180 = Image.open(figure2.visualFilename).transpose(Image.ROTATE_180)
    rotate270 = Image.open(figure2.visualFilename).transpose(Image.ROTATE_270)

    if equality(source, rotate90):
        return 'rotated_90'
    elif equality(source, rotate180):
        return 'rotated_180'
    elif equality(source, rotate270):
        return 'rotated_270'
    else:
        return None


def get_transformation(figure1, figure2):

    transformations = {}
    rotated = rotation(figure1, figure2)

    transformations['equality'] = equality(figure1, figure2)
    transformations['h_flip'] = h_flip(figure1, figure2)
    transformations['v_flip'] = v_flip(figure1, figure2)
    transformations['rotation'] = rotation(figure1, figure2)
    transformations['shape_delta'] = shape_delta(figure1, figure2)

    return transformations


def create_2x2_network(figures):
    networks = {}
    networks['horizontal'] = []
    networks['vertical'] = []

    # 0  1
    # 2  3

    # a  b
    # c  solution

    # horizontal
    for i in range(len(figures) - 1):

        if i == 1:
            continue

        semantic_network = {}
        name = figures[i].name + '->' + figures[i + 1].name
        semantic_network[name] = get_transformation(figures[i], figures[i + 1])
        # print(semantic_network)
        networks['horizontal'].append(semantic_network)

    # vertical
    for i in range(len(figures) - 2):

        semantic_network = {}
        name = figures[i].name + '->' + figures[i + 2].name
        semantic_network[name] = get_transformation(figures[i], figures[i + 2])
        # print(semantic_network)
        networks['vertical'].append(semantic_network)

    return networks


def create_3x3_network(figures):

    networks = {}
    networks['horizontal'] = []
    networks['vertical'] = []
    networks['diagonal'] = []

    # 0  1  3
    # 4  5  6
    # 7  8  9

    # a  b  c
    # d  e  f
    # g  h  solution

    # horizontal
    for i in range(len(figures) - 1):

        if i == 2 or i == 5:
            continue

        semantic_network = {}
        name = figures[i].name + '->' + figures[i + 1].name
        semantic_network[name] = get_transformation(figures[i], figures[i + 1])
        # print(semantic_network)
        networks['horizontal'].append(semantic_network)

    # vertical
    for i in range(len(figures) - 3):

        semantic_network = {}
        name = figures[i].name + '->' + figures[i + 3].name
        semantic_network[name] = get_transformation(figures[i], figures[i + 3])
        # print(semantic_network)
        networks['vertical'].append(semantic_network)

    # diagonal
    for i in range(len(figures) - 4):
        if i == 0 or i == 5:
            semantic_network = {}
            name = figures[i].name + '->' + figures[i + 4].name
            semantic_network[name] = get_transformation(figures[i], figures[i + 4])
            # print(semantic_network)
            networks['diagonal'].append(semantic_network)

    return networks


def create_semantic_network(figures, type):

    if type == '3x3':
        return create_3x3_network(figures)
    else:
        return create_2x2_network(figures)


def agent_compare(init_network, solution_network, problemType):
    pass


def normalize_scores(scores):

    t = float(sum(scores))
    out = [x / t for x in scores]
    return out


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().]

    def __init__(self):
        pass

    def Solve(self, problem):

        figures = None
        solutions = None

        setup(problem, figures, solutions)

        # generate our initial semantic network to test against
        init_network = create_semantic_network(figures, problem.problemType)

        scores = []

        for solution in solutions:

            compare_figures = figures
            compare_figures.append(solution)
            # compare init_network with generated solutions
            solution_network = create_semantic_network(compare_figures, problem.problemType)

            score = agent_compare(init_network, solution_network, problem.problemType)
            scores.append(score)

        scores = normalize_scores(scores)

        print(scores)
        print('given answer: ' + str(scores.index(max(scores)) + 1))
        print('actual answer: ' + str(problem.checkAnswer(scores)))
        print()
        return scores
