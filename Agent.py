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

# http://blog.lexique-du-net.com/index.php?post/Calculate-the-real-difference-between-two-angles-keeping-the-sign
def calcDistanceBetweenTwoAngles(angle1, angle2):

    angle1 = int(angle1)
    angle2 = int(angle2)

    difference = angle2 - angle1

    if difference < -180:
        difference += 360
    if difference > 180:
        difference -= 360

    return abs(difference)

def calcAlignment(keyword1, keyword2, orientation):

    if orientation == 'horizontal':
        if keyword1 == 'bottom-right' and keyword2 == 'bottom-left':
            return 'mirrored'
        elif keyword1 == 'top-right' and keyword2 == 'top-left':
            return 'mirrored'
        else:
            return keyword1 + '->' + keyword2

    elif orientation == 'vertical':
        if keyword1 == 'bottom-right' and keyword2 == 'top-right':
            return 'mirrored'
        elif keyword1 == 'bottom-left' and keyword2 == 'top-left':
            return 'mirrored'
        else:
            return keyword1 + '->' + keyword2

def findByAttribute(figure, attribute):

    for objectName in figure.objects:
        thisObject = figure.objects[objectName]
        if attribute in thisObject.attributes:
            return thisObject

def getFirstItem(ravensFigure):
    return next (iter (ravensFigure.objects.values()))

def excludeByAttribute(figure, attribute):

    for objectName in figure.objects:
        thisObject = figure.objects[objectName]
        if attribute not in thisObject.attributes:
            return thisObject


def transformUtility(transformationDict, prop, obj1, obj2):

    if prop in obj1.attributes and prop in obj2.attributes:
        if obj1.attributes[prop] == obj2.attributes[prop]:
            transformationDict[prop] = 'unchanged'
        else:

            if prop == 'angle':
                transformationDict[prop] = calcDistanceBetweenTwoAngles(obj1.attributes[prop], obj2.attributes[prop])
            elif prop == 'alignment':
                transformationDict[prop] = calcAlignment(obj1.attributes[prop],
                                                         obj2.attributes[prop], transformationDict['orientation'])
            else:
                transformationDict[prop] = obj1.attributes[prop] + '->' + obj2.attributes[prop]

def createSingleTransformationNetwork(figure1, figure2, orientation):

    transformation = dict()
    transformation['orientation'] = orientation
    transformation['type'] = 'single'

    for prop in ['shape', 'size', 'fill', 'angle', 'alignment']:
        transformUtility(transformation, prop, getFirstItem(figure1), getFirstItem(figure2))
    return transformation

def createDoubleTransformationNetwork(master_figures, relational_figures, orientation):

    transformations = dict()
    transformations['type'] = 'multiple'

    master_transformation = dict()
    master_transformation['orientation'] = orientation

    relational_transformation = dict()
    relational_transformation['orientation'] = orientation

    for prop in ['shape', 'size', 'fill', 'angle', 'alignment']:

        transformUtility(master_transformation, prop, master_figures[0], master_figures[1])

        if len(relational_figures) <= 1:
            relational_transformation['transformation'] = 'removed'
        else:
            transformUtility(relational_transformation, prop, relational_figures[0], relational_figures[1])

    transformations['master'] = master_transformation
    transformations['relational'] = relational_transformation
    return transformations


def createSemanticNetwork(figure_i, figure_j, orientation):
    # construct a semantic network showing the transformation that occurred between figure i -> j
    if len(figure_i.objects) == 1 and len(figure_j.objects) == 1:
        transformation = createSingleTransformationNetwork(figure_i, figure_j, orientation)
        return transformation

    # 2 shapes, need to match by attributes, e.g. 'inside'
    else:

        relational_keyword = None
        relational_figures = []
        master_figures = []

        # get relational matches first
        for objectName in figure_i.objects:
            thisObject = figure_i.objects[objectName]

            for attributeName in thisObject.attributes:

                if attributeName == 'inside':
                    relational_keyword = 'inside'
                    relationalObject = findByAttribute(figure_j, 'inside')
                    relational_figures.append(thisObject)
                    relational_figures.append(relationalObject)

        master_figures.append(excludeByAttribute(figure_i, relational_keyword))
        master_figures.append(excludeByAttribute(figure_j, relational_keyword))

        transformations = createDoubleTransformationNetwork(master_figures, relational_figures, orientation)
        return transformations


def agentCompare(init_network, solution_network):

    if init_network[0]['type'] == 'single':
        # print('a -> b')
        # print(init_network[0])
        # print('a -> c')
        # print(init_network[1])
        # print('\n')
        #
        # print('c -> solution')
        # print(solution_network[0])
        # print('b -> solution')
        # print(solution_network[1])
        # print('\n')

        shared_items1 = set(init_network[0].items()) & set(
            solution_network[0].items())

        shared_items2 = set(init_network[1].items()) & set(
            solution_network[1].items())

        # print(str(len(shared_items1)) + ' matches horizontally')
        # print(str(len(shared_items2)) + ' matches vertically')

        return len(shared_items1) + len(shared_items2)

    else:

        print('a -> b')
        print(init_network[0]['master'])
        print(init_network[0]['relational'])
        print('a -> c')
        print(init_network[1]['master'])
        print(init_network[1]['relational'])
        print('\n')

        print('c -> solution')
        print(solution_network[0]['master'])
        print(solution_network[0]['relational'])
        print('b -> solution')
        print(solution_network[1]['master'])
        print(solution_network[1]['relational'])
        print('\n')

        master_shared1 = set(init_network[0]['master'].items() & solution_network[0]['master'].items())
        master_shared2 = set(init_network[1]['master'].items() & solution_network[1]['master'].items())

        relational_shared1 = set(init_network[0]['relational'].items() & solution_network[0]['relational'].items())
        relational_shared2 = set(init_network[1]['relational'].items() & solution_network[1]['relational'].items())

        return len(master_shared1) + len(master_shared2) + len(relational_shared1) + len(relational_shared2)


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
        if problem.problemType == '3x3':
            return [.1, .1, .1, .1, .1, .1]
        if problem.hasVerbal == False:
            return [.1, .1, .1, .1, .1, .1]

        a = problem.figures["A"]
        b = problem.figures["B"]
        c = problem.figures["C"]

        _1 = problem.figures["1"]
        _2 = problem.figures["2"]
        _3 = problem.figures["3"]
        _4 = problem.figures["4"]
        _5 = problem.figures["5"]
        _6 = problem.figures["6"]

        # generate our initial semantic network to test against
        init_network = [createSemanticNetwork(
            a, b, 'horizontal'), createSemanticNetwork(a, c, 'vertical')]

        # all possible solutions
        solutions = [_1, _2, _3, _4, _5, _6]
        scores = []

        for solution in solutions:
            print('\n')
            print('comparing with solution ' + solution.name)
            # compare init_network with generated solutions
            solution_network = [createSemanticNetwork(
                c, solution, 'horizontal'), createSemanticNetwork(b, solution, 'vertical')]

            score = agentCompare(init_network, solution_network)
            scores.append(score)

        t = float(sum(scores))
        out = [x / t for x in scores]

        print(out)
        print('given answer: ' + str(scores.index(max(scores)) + 1))
        print('actual answer: ' + str(problem.checkAnswer(out)))

        return out
