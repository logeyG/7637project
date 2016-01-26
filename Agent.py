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

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    def createSemanticNetwork(i, j, k):

        # compare and determine if horizontal / vertical tranformation was used ?
        # compare shape, fill, size
        i_j_transformation = {}
        j_k_transformation = {}

        # shape
        if i['shape'] == j['shape']:
            i_j_transformation.shape = 'unchanged'
        else:
            i_j_transformation.shape = i['shape'] +  ' -> ' + j['shape']

        # fill
        if i['fill'] == j['fill']:
            i_j_transformation.fill = 'unchanged'
        else:
            i_j_transformation.fill = 'inverted'

        # size
        if i['size'] == j['size']:
            i_j_transformation.size = 'unchanged'
        else:
            i_j_transformation.size = i['size'] + ' -> ' + j['size']

        # now look at extra properties
        # what if there's more than shape, fill, and size ? 
   
        # shape
        if i['shape'] == k['shape']:
            j_k_transformation.shape = 'unchanged'
        else:
            j_k_transformation.shape = i['shape'] +  ' -> ' + k['shape']

        # fill
        if i['fill'] == k['fill']:
            j_k_transformation.fill = 'unchanged'
        else:
            j_k_transformation.fill = 'inverted'

        # size
        if i['size'] == k['size']:
            j_k_transformation.size = 'unchanged'
        else:
            j_k_transformation.size = i['size'] + ' -> ' + k['size']

        return [i_j_transformation, j_k_transformation]

    def agentCompare(init_network, solution_network):

        # how to intelligently compare two networks?
        return -1

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a list representing its
    # confidence on each of the answers to the question: for example 
    # [.1,.1,.1,.1,.5,.1] for 6 answer problems or [.3,.2,.1,.1,0,0,.2,.1] for 8 answer problems.
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(int givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will *not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):

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

        problem.checkAnswer()
        return scores