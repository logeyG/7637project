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
def calc_distance_between_two_angles(angle1, angle2):

    angle1 = int(angle1)
    angle2 = int(angle2)

    difference = angle2 - angle1

    if difference < -180:
        difference += 360
    if difference > 180:
        difference -= 360

    return abs(difference)


def calc_alignment(keyword1, keyword2, orientation):

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


def get_first_item(figure):
    return next (iter (figure.objects.values()))


def transform_utility(transformation_dict, prop, obj1, obj2):

    t_key = obj1.name + '->' + obj2.name
    transformation_dict[t_key] = {}

    if prop in obj1.attributes and prop in obj2.attributes:
        if obj1.attributes[prop] == obj2.attributes[prop]:
            transformation_dict[t_key][prop] = 'unchanged'
        else:

            if prop == 'angle':
                transformation_dict[t_key][prop] = calc_distance_between_two_angles(obj1.attributes[prop], obj2.attributes[prop])
            elif prop == 'alignment':
                transformation_dict[t_key][prop] = calc_alignment(obj1.attributes[prop],
                                                         obj2.attributes[prop], transformation_dict['orientation'])
            else:
                transformation_dict[t_key][prop] = obj1.attributes[prop] + '->' + obj2.attributes[prop]


def create_transformation_network(figure_i, figure_j, figure_mapping, orientation):

    transformation = dict()
    transformation['orientation'] = orientation
    transformation['transformation'] = figure_i.name + '->' + figure_j.name

    for key, value in figure_mapping.items():
        for prop in ['shape', 'size', 'fill', 'angle', 'alignment']:
            transform_utility(transformation, prop, figure_i.objects[key], figure_j.objects[value])

    return transformation


def find_partner_object_by_attribute(figure, relational_size, attributeName):

    for objectName in figure.objects:
        thisObject = figure.objects[objectName]

        if attributeName in thisObject.attributes:
            if len(thisObject.attributes[attributeName].split(',')) == relational_size:
                return thisObject.name

    return None

def find_partner_object(figure, keywords):

    for objectName in figure.objects:
        thisObject = figure.objects[objectName]
        for attributeName in thisObject.attributes:

             if attributeName not in keywords:
                 return thisObject.name

    return None

def create_semantic_network(figure_i, figure_j, orientation, title):

    if len(figure_i.objects) == 1 and len(figure_j.objects) == 1:

        figure_mapping = {}
        figure_mapping[get_first_item(figure_i).name] = get_first_item(figure_j).name

        transformation = create_transformation_network(figure_i, figure_j, figure_mapping, orientation)
        return transformation

    else:

        keywords = ['inside', 'above']
        figure_mapping = {}

        # get relational matches first
        for objectName in figure_i.objects:
            thisObject = figure_i.objects[objectName]

            for attributeName in thisObject.attributes:

                if attributeName in keywords:
                    relational_size = len(thisObject.attributes[attributeName].split(','))
                    figure_mapping[objectName] = find_partner_object_by_attribute(figure_j,
                                                                                  relational_size, attributeName)
                else:
                    figure_mapping[objectName] = find_partner_object(figure_j, keywords)

        transformations = create_transformation_network(figure_i, figure_j, figure_mapping, orientation)

        return transformations


def agent_compare(init_network, solution_network):

        shared_items1 = set(init_network[0].items()) & set(
            solution_network[0].items())

        shared_items2 = set(init_network[1].items()) & set(
            solution_network[1].items())

        return len(shared_items1) + len(shared_items2)


def normalize_scores(scores, semantic_network):

    # represents an exact match
    # max_score = len(semantic_network[0]) * 2
    #
    # for i, score in enumerate(scores):
    #     if score != max_score:
    #         scores[i] = 0

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

        if problem.problemType == '3x3':
            return [.1, .1, .1, .1, .1, .1]
        if problem.hasVerbal is False:
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
        init_network = [create_semantic_network(
            a, b, 'horizontal', 'init'), create_semantic_network(a, c, 'vertical', 'init')]

        # all possible solutions
        solutions = [_1, _2, _3, _4, _5, _6]
        scores = []

        for solution in solutions:
            # compare init_network with generated solutions
            solution_network = [create_semantic_network(
                c, solution, 'horizontal', solution.name), create_semantic_network(b, solution, 'vertical', solution.name)]

            score = agent_compare(init_network, solution_network)
            scores.append(score)

        scores = normalize_scores(scores, init_network)

        print(scores)
        print('given answer: ' + str(scores.index(max(scores)) + 1))
        print('actual answer: ' + str(problem.checkAnswer(scores)))
        print('\n')

        return scores
