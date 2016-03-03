# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
from PIL import ImageChops


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


def equality(figure1, figure2):
    # http://effbot.org/zone/pil-comparing-images.htm#rms
    # calculate the root-mean-square difference between two images
    h = ImageChops.difference(figure1, figure2).histogram()
    # calculate rms
    equality = math.sqrt(reduce(operator.add,
                                map(lambda h, i: h * (i**2), h, range(256))
                                ) / (float(figure1.size[0]) * figure1.size[1]))
    if equality < 0.1:
        return True
    else:
        return False


def h_flip(figure1, figure2):
    source = Image.open(figure1)
    flipped = Image.open(figure2.visualFilename).transpose(Image.FLIP_LEFT_RIGHT)
    return calc_equality(source, flipped)


def v_flip(figure1, figure2):
    source = Image.open(figure1)
    flipped = Image.open(figure2.visualFilename).transpose(Image.FLIP_TOP_BOTTOM)
    return calc_equality(source, flipped)


def rotation(figure1, figure2):
    source = Image.open(figure1)
    rotate90 = Image.open(figure2.visualFilename).transpose(Image.ROTATE_90)
    rotate180 = Image.open(figure2.visualFilename).transpose(Image.ROTATE_180)
    rotate270 = Image.open(figure2.visualFilename).transpose(Image.ROTATE_270)

    if calc_equality(source, rotate90):
        return (True, '90')
    elif calc_equality(source, rotate180):
        return (True, '180')
    elif calc_equality(source, rotate270):
        return (True, '270')
    else:
        return False


def create_semantic_network(nodes):

    # need to analyze
    # horizontal
    # a -> b, b -> c
    # d -> e, e -> f
    # g -> h, h -> solution

    # 0 -> 1, 1 -> 2
    # 3 -> 4, 4 -> 5
    # 6 -> 7, 7 -> 8

    # vertical
    # a -> d, d -> g
    # b -> e, e -> h
    # c -> f, f -> solution

    # 0 -> 3, 3 -> 6
    # 1 -> 4, 4 -> 7
    # 2 -> 5, 5 -> 8

    # diagonal
    # a -> e, e -> solution
    # 0 -> 4, 4 -> 8

    for node in nodes:
        print node.name


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
