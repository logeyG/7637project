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
#from PIL import Image
def createSemanticNetwork(i, j, k):

    # compare and determine if horizontal / vertical tranformation was used ?
    # compare shape, fill, size
    i_j_transformation = {}
    j_k_transformation = {}

    # shape
    if i['shape'] == j['shape']:
        i_j_transformation['shape'] = 'unchanged'
    else:
        i_j_transformation['shape'] = i['shape'] +  ' -> ' + j['shape']

    # fill
    if i['fill'] == j['fill']:
        i_j_transformation['fill'] = 'unchanged'
    else:
        i_j_transformation['fill'] = 'inverted'

    # size
    if i['size'] == j['size']:
        i_j_transformation['size'] = 'unchanged'
    else:
        i_j_transformation['size'] = i['size'] + ' -> ' + j['size']

    # now look at extra properties
    # what if there's more than shape, fill, and size ? 

    # shape
    if i['shape'] == k['shape']:
        j_k_transformation['shape'] = 'unchanged'
    else:
        j_k_transformation['shape'] = i['shape'] +  ' -> ' + k['shape']

    # fill
    if i['fill'] == k['fill']:
        j_k_transformation['fill'] = 'unchanged'
    else:
        j_k_transformation['fill'] = 'inverted'

    # size
    if i['size'] == k['size']:
        j_k_transformation['size'] = 'unchanged'
    else:
        j_k_transformation['size'] = i['size'] + ' -> ' + k['size']

    return [i_j_transformation, j_k_transformation]

def agentCompare(init_network, solution_network):
    shared_items1 = set(init_network[0].items()) & set(solution_network[0].items())
    shared_items2 = set(init_network[1].items()) & set(solution_network[1].items())
    return len(shared_items1) + len(shared_items2)


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    def Solve(self,problem):

        if problem.problemType == '3x3':
            return -1

        # RavensProblem.RavensFigure.RavensObject
        a = problem.figures["A"].objects['a'].attributes
        b = problem.figures["B"].objects['b'].attributes
        c = problem.figures["C"].objects['c'].attributes

        _1 = problem.figures["1"].objects['d'].attributes
        _2 = problem.figures["2"].objects['e'].attributes
        _3 = problem.figures["3"].objects['f'].attributes
        _4 = problem.figures["4"].objects['g'].attributes
        _5 = problem.figures["5"].objects['h'].attributes
        _6 = problem.figures["6"].objects['i'].attributes

        # generate our initial semantic network to test against
        init_network = createSemanticNetwork(a, b, c)

        # all possible solutions
        solutions = [_1, _2, _3, _4, _5, _6]
        scores = []

        for solution in solutions:
            # compare init_network with generated solutions
            solution_network = createSemanticNetwork(b, c, solution)
            score = agentCompare(init_network, solution_network)
            scores.append(score)

        t = float(sum(scores))
        out = [x/t for x in scores]
        
        print(out)
        print('given answer: ' + str(scores.index(max(scores)) + 1))
        print('actual answer: ' + str(problem.checkAnswer(out)))

        return out