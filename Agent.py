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


def setup(problem):

    figures = None
    solutions = None
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

    return figures, solutions


def dict_compare(d1, d2):
    # solution from
    # http://stackoverflow.com/questions/4527942/comparing-two-dictionaries-in-python
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same

def find_first_edge(figure):

    img = Image.open(figure.visualFilename)
    pixels = img.load()

    width, height = img.size
    pixels = img.load()
    # first pass. find regions.
    for x in range(width):
        for y in range(height):
            # look for a black pixel
            if pixels[x, y] == (0, 0, 0, 255):  # black pixel
                return (x, y)

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


def similarity(source, compare):

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

    return round(equality, 0)

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
    if round(equality, 0) < 40.0:
        return True
    else:
        return False

def edge_comparison(source, compare):

    source_distance = round(math.sqrt( math.pow(find_first_edge(source)[0], 2)
                                       + math.pow(find_first_edge(source)[1], 2 )), 0)
    compare_distance = round(math.sqrt( math.pow(find_first_edge(compare)[0], 2)
                                        + math.pow(find_first_edge(compare)[1], 2 )), 0)

    if source_distance > compare_distance and (source_distance - compare_distance > 5):
        return 'expanded'
    elif source_distance < compare_distance and (compare_distance - source_distance > 5):
        return 'contracted'
    else:
        return 'unchanged'


def shape_delta(source, compare):
    source_count = len(find_regions(source))
    compare_count = len(find_regions(compare))

    if source_count < compare_count:
        return 'added' #+ str(compare_count - source_count)
    elif source_count > compare_count:
        return 'removed' #+ str(source_count - compare_count)
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

    if h_flip(figure1, figure2):
        transformations['h_flip'] = True

    if v_flip(figure1, figure2):
        transformations['v_flip'] = True

    if rotation(figure1, figure2) != None:
        transformations['rotation'] = rotation(figure1, figure2)

    if edge_comparison(figure1, figure2) != 'unchanged':
        transformations['edge_comparison'] = edge_comparison(figure1, figure2)

    transformations['equality'] = equality(figure1, figure2)
    transformations['shape_delta'] = shape_delta(figure1, figure2)

    return transformations


def create_2x2_network(figures):
    pass
    # 0  1
    # 2  3

    # a  b
    # c  solution


def create_relationship_diagram(figures):

    relationship_diagrams = []
    if len(figures) == 2:
        pass
    else:
        for i in range(len(figures) - 1):
            relationship_diagrams.append(get_transformation(figures[i], figures[i + 1]))

    return relationship_diagrams


def create_3x3_network(figures):

    # 0  1  3
    # 4  5  6
    # 7  8  9

    # a  b  c
    # d  e  f
    # g  h  solution

    H1 = create_relationship_diagram([figures[0], figures[1], figures[2]])
    H2 = create_relationship_diagram([figures[3], figures[4], figures[5]])
    V1 = create_relationship_diagram([figures[0], figures[3], figures[6]])
    V2 = create_relationship_diagram([figures[1], figures[4], figures[7]])
    R = (H1, H2, V1, V2)

    return R


def create_semantic_network(figures, problem):

    if problem.problemType == '3x3':
        return create_3x3_network(figures)
    else:
        return create_2x2_network(figures)


def get_similarity_metric(a, b):

    added_h, removed_h, modified_h, same_h = dict_compare(a[0], b[0])
    added_v, removed_v, modified_v, same_v = dict_compare(a[1], b[1])

    return weighted_score(same_h) + weighted_score(same_v)

def weighted_score(s):

    score = 0

    for label in s:
        score +=1

    return score


def agent_compare(init_network, H, V, problem, solution_num):

    if problem.problemType == '3x3':

        H1 = init_network[0]
        H2 = init_network[1]

        V1 = init_network[2]
        V2 = init_network[3]

        metrics = [get_similarity_metric(H1, H),
                   get_similarity_metric(H2, H),
                   get_similarity_metric(V1, V),
                   get_similarity_metric(V2, V)]

        result = float(sum(metrics))
        return result

    else:

        result = [1, 2, 3, 4, 5, 6]
        return result


def normalize_scores(scores):

    t = float(sum(scores))

    if t == 0:
        out = [.125, .125, .125, .125, .125, .125, .125, .125]
    else:

        m_score = max(scores)
        for i, score in enumerate(scores):
            if score != m_score:
                scores[i] = 0

        t = float(sum(scores))
        out = [x / t for x in scores]

    return out

def pick_one(scores, figures, solutions):

    comparisons = []
    for i, score in enumerate(scores):

        if score != 0.0:
            x = (i, similarity(figures[7], solutions[i]))
            comparisons.append(x)

    m = min(comparisons, key = lambda t: t[1])

    scores = [0, 0, 0, 0, 0, 0, 0, 0]
    scores[m[0]] = 1

    return scores


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().]

    def __init__(self):
        pass

    def Solve(self, problem):

        figures, solutions = setup(problem)

        # generate our initial semantic network to test against
        init_network = create_semantic_network(figures, problem)

        scores = []

        for i, solution in enumerate(solutions):

            # compare init_network with generated solutions
            H = create_relationship_diagram([figures[6], figures[7], solution])
            V = create_relationship_diagram([figures[2], figures[5], solution])

            score = agent_compare(init_network, H, V, problem, i + 1)
            scores.append(score)

        scores = normalize_scores(scores)
        print(scores)

        if 1.0 not in scores:
            scores = pick_one(scores, figures, solutions)

        print(scores)
        print('given answer: ' + str(scores.index(max(scores)) + 1))
        print('actual answer: ' + str(problem.checkAnswer(scores)))
        print()
        return scores
