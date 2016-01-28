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
# from PIL import Image

relational_keywords = ['inside', 'above', 'below']


def excludeByProperty(d, prop):
    for key, value in d.items():
        if prop not in value.attributes:
            return value


def findByProperty(d, prop):
    for key, value in d.items():
        if prop in value.attributes:
            return value


def createSemanticNetwork(i, j):
    # construct a semantic network showing the transformation that occured
    # between frame i -> j
    tranformation = {}
    # loop through all shapes in i
    for key, value in i.items():
        if 'inside' in value.attributes:
            # match this shape with the shape containing 'inside' in the other object
            match = findByProperty(j, 'inside')

            # we've found matches, now lets loop through their attributes and see what transformed
        else:
            # this is another shape that is not inside, match this with corresponding
            match2 = excludeByProperty(j, 'inside')

    if i['shape'] == j['shape']:
        transformation['shape'] = 'unchanged'
    else:
        transformation['shape'] = i['shape'] + ' -> ' + j['shape']

    if i['fill'] == j['fill']:
        transformation['fill'] = 'unchanged'
    else:
        transformation['fill'] = 'inverted'

    if i['size'] == j['size']:
        transformation['size'] = 'unchanged'
    else:
        transformation['size'] = i['size'] + ' -> ' + j['size']

    return tranformation


def agentCompare(init_network, solution_network):

    print('horizontal')
    print('a -> b')
    print(init_network[0])
    print('c -> solution')
    print(solution_network[1])
    print('\n')
    print('vertical')
    print('a -> c')
    print(init_network[1])
    print('b -> solution')
    print(solution_network[0])
    print('\n')

    shared_items1 = set(init_network[0].items()) & set(
        solution_network[1].items())

    shared_items2 = set(init_network[1].items()) & set(
        solution_network[0].items())

    print(str(len(shared_items1)) + ' matches horizontally')
    print(str(len(shared_items2)) + ' matches vertically')

    return len(shared_items1) + len(shared_items2)


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().]

    def __init__(self):
        pass

    def Solve(self, problem):

        if problem.problemType == '3x3':
            return -1

        if problem.name != 'Basic Problem B-02':
            return -1

        a = problem.figures["A"].objects
        b = problem.figures["B"].objects
        c = problem.figures["C"].objects

        _1 = problem.figures["1"].objects
        _2 = problem.figures["2"].objects
        _3 = problem.figures["3"].objects
        _4 = problem.figures["4"].objects
        _5 = problem.figures["5"].objects
        _6 = problem.figures["6"].objects

        # generate our initial semantic network to test against
        init_network = [createSemanticNetwork(
            a, b), createSemanticNetwork(a, c)]

        # all possible solutions
        solutions = [_1, _2, _3, _4, _5, _6]
        scores = []

        for solution in solutions:
            # compare init_network with generated solutions
            solution_network = [createSemanticNetwork(
                c, solution), createSemanticNetwork(b, solution)]
            score = agentCompare(init_network, solution_network)
            scores.append(score)

        t = float(sum(scores))
        out = [x / t for x in scores]

        print(out)
        print('given answer: ' + str(scores.index(max(scores)) + 1))
        print('actual answer: ' + str(problem.checkAnswer(out)))

        return out
