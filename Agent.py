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


# solution adapted from this stackoverflow post
# http://stackoverflow.com/questions/14263050/
# segment-an-image-using-python-and-pil-to-calculate-centroid-and-rotations-of-mul
def follow_border(im, x, y, used):
    work = [(x, y)]
    border = []
    while work:
        x, y = work.pop()
        used.add((x, y))
        border.append((x, y))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1),
                       (1, 1), (-1, -1), (1, -1), (-1, 1)):
            px, py = x + dx, y + dy
            if im[px, py] == 255 or (px, py) in used:
                continue
            work.append((px, py))

    return border


def rmsdiff(figure1, figure2):
    # http://effbot.org/zone/pil-comparing-images.htm#rms
    # calculate the root-mean-square difference between two images
    h = ImageChops.difference(figure1, figure2).histogram()

    # calculate rms
    return math.sqrt(reduce(operator.add,
                            map(lambda h, i: h * (i**2), h, range(256))
                            ) / (float(figure1.size[0]) * figure1.size[1]))


def shape_count(figure):

    img = Image.open(figure.visualFilename)
    pixels = img.load()

    width, height = img.size

    used = set()
    border = []
    for x in range(width):
        for y in range(height):
            thisPixel = pixels[x, y]
            if thisPixel == 255 or (x, y) in used:
                continue
            b = follow_border(pixels, x, y, used)
            border.append(b)

    return len(border)


def create_semantic_network(nodes):
    for node in nodes:
        print(shape_count(node))


def agent_compare(init_network, solution_network):
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

        print('solving problem ' + problem.name)

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

        # generate our initial semantic network to test against
        init_network = create_semantic_network([a, b, c, d, e, f, g, h])
        # all possible solutions
        solutions = [_1, _2, _3, _4, _5, _6, _7, _8]
        scores = []

        for solution in solutions:

            # compare init_network with generated solutions
            solution_network = create_semantic_network([a, b, c, d, e, f, g, h, solution])

            score = agent_compare(init_network, solution_network)
            scores.append(score)

        scores = normalize_scores(scores)

        print(scores)
        print('given answer: ' + str(scores.index(max(scores)) + 1))
        print('actual answer: ' + str(problem.checkAnswer(scores)))
        print()
        return scores
