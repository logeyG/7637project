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
    return next(iter (figure.objects.values()))


def transform_utility(transformation_dict, prop, obj1, obj2):

    t_key = obj1.name + '->' + obj2.name
    if t_key not in transformation_dict:
        transformation_dict[t_key] = {}

    if prop in obj1.attributes and prop in obj2.attributes:
        if obj1.attributes[prop] == obj2.attributes[prop]:
            transformation_dict[t_key][prop] = 'unchanged'
        else:

            if prop == 'angle':
                transformation_dict[t_key][prop] = calc_distance_between_two_angles(obj1.attributes[prop],
                                                                                    obj2.attributes[prop])
            elif prop == 'alignment':
                transformation_dict[t_key][prop] = calc_alignment(obj1.attributes[prop],
                                                         obj2.attributes[prop], transformation_dict['orientation'])
            else:
                transformation_dict[t_key][prop] = obj1.attributes[prop] + '->' + obj2.attributes[prop]


def create_transformation_network(figure_i, figure_j, figure_mapping, orientation):

    transformation = dict()
    transformation['orientation'] = orientation
    transformation['transformation'] = figure_i.name + '->' + figure_j.name
    transformation['mapping'] = figure_mapping

    for key, value in figure_mapping.items():
        for prop in ['shape', 'size', 'fill', 'angle', 'alignment']:

            if value['type'] != 'removed' and value['type'] != 'added':
                transform_utility(transformation, prop, figure_i.objects[key], figure_j.objects[value['name']])

    return transformation


def find_partner_object_by_attribute(object, figure, relational_size, attributeName):

    for objectName in figure.objects:
        thisObject = figure.objects[objectName]

        if attributeName in thisObject.attributes:
            if len(thisObject.attributes[attributeName].split(',')) == relational_size:

                obj = dict()
                obj['name'] = thisObject.name
                obj['type'] = 'relational'
                obj['keyword'] = attributeName
                obj['size'] = relational_size
                return obj

    # if didn't find anything there then just try a more generalized approach
    for objectName in figure.objects:
        thisObject = figure.objects[objectName]

        if attributeName in thisObject.attributes:
            obj = dict()
            obj['name'] = thisObject.name
            obj['type'] = 'relational'
            obj['keyword'] = attributeName
            obj['size'] = 1
            return obj

    obj = dict()
    obj['name'] = ''
    obj['type'] = 'removed'
    return obj


def find_partner_object(mapped_object, figure, keywords):

    for objectName in figure.objects:
        thisObject = figure.objects[objectName]
        shared_keywords = set(thisObject.attributes) & set(keywords)
        if len(shared_keywords) == 0:
            obj = dict()
            obj['name'] = thisObject.name
            obj['type'] = 'master'
            return obj

    obj = dict()
    obj['name'] = ''
    obj['type'] = 'removed'
    return obj


def create_figure_mapping(mapped_object, figure, keywords):

    shared_keywords = set(mapped_object.attributes) & set(keywords)

    if len(shared_keywords) > 0:
        for attrib in shared_keywords:
            relational_size = len(mapped_object.attributes[attrib].split(','))
            return find_partner_object_by_attribute(mapped_object, figure, relational_size, attrib)

    else:
        return find_partner_object(mapped_object, figure, keywords)


def create_semantic_network(figure_i, figure_j, orientation, title):

    keywords = ['inside', 'above', 'overlap']
    figure_mapping = {}

    for objectName in figure_i.objects:
        thisObject = figure_i.objects[objectName]
        figure_mapping[objectName] = create_figure_mapping(thisObject, figure_j, keywords)

    # find additions
    for objectName in figure_j.objects:
        thisObject = figure_j.objects[objectName]

        keys = []
        values = []
        for key, value in figure_mapping.items():
            keys.append(key)
            values.append(value['name'])

        if thisObject.name not in keys and thisObject.name not in values:
            obj = dict()
            obj['type'] = 'added'
            obj['name'] = ''
            figure_mapping[thisObject.name] = obj

    transformation = create_transformation_network(figure_i, figure_j, figure_mapping, orientation)
    transformation['mapping'] = figure_mapping
    return transformation

def create_compare_figure_mapping(horizontal_mapping, vertical_mapping, init_network, solution_network):

    # compare horizontal transformation
    for key, value in init_network[0]['mapping'].items():
        for key2, value2 in solution_network[0]['mapping'].items():
            if value['type'] == value2['type']:
                if value['type'] == 'relational':
                    if value['keyword'] == value2['keyword'] and value['size'] == value2['size']:
                        horizontal_mapping[key + '->' + value['name']] = key2 + '->' + value2['name']
                elif value['type'] == 'master':
                    horizontal_mapping[key + '->' + value['name']] = key2 + '->' + value2['name']

    # compare vertical transformation
    for key, value in init_network[1]['mapping'].items():
        for key2, value2 in solution_network[1]['mapping'].items():
            if value['type'] == value2['type']:
                if value['type'] == 'relational':
                    if value['keyword'] == value2['keyword'] and value['size'] == value2['size']:
                        vertical_mapping[key + '->' + value['name']] = key2 + '->' + value2['name']
                elif value['type'] == 'master':
                    vertical_mapping[key + '->' + value['name']] = key2 + '->' + value2['name']


def agent_compare(init_network, solution_network):

    horizontal_mapping = dict()
    horizontal_score = 0

    vertical_mapping = dict()
    vertical_score = 0

    create_compare_figure_mapping(horizontal_mapping, vertical_mapping, init_network, solution_network)

    for key, value in horizontal_mapping.items():
        horizontal_score += len(set(init_network[0][key].items()) & set(solution_network[0][value].items()))

    for key, value in vertical_mapping.items():
        vertical_score += len(set(init_network[1][key].items()) & set(solution_network[1][value].items()))

    return horizontal_score + vertical_score


def normalize_scores(scores):

    max_score = max(scores)
    for i, value in enumerate(scores):
        if value != max_score:
            scores[i] = 0

    t = float(sum(scores))

    # no answer could be found
    if t == 0:
        scores = [1, 1, 1, 1, 1, 1]
        t = float(sum(scores))
        out = [x / t for x in scores]
        return out

    out = [x / t for x in scores]
    return out

def prune_solution(init_network, solution_network):
    return False

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

            prune = prune_solution(init_network, solution_network)

            if prune:
                score = 0
            else:
                score = agent_compare(init_network, solution_network)
            scores.append(score)

        scores = normalize_scores(scores)

        print(scores)
        print('given answer: ' + str(scores.index(max(scores)) + 1))
        # print('actual answer: ' + str(problem.checkAnswer(scores)))
        print()
        return scores
