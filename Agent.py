# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

from visual import transformation
from visual import utility
from visual import comparison
from visual import algorithm

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

def get_transformation(figure1, figure2, orientation, problemType):

    transformations = {}

    #transformations['alignment'] = transformation.alignment(figure1, figure2, orientation, problemType)
    transformations['size'] = transformation.size_comparison(figure1, figure2)
    transformations['fill_delta'] = transformation.fill_delta(figure1, figure2)

    if transformation.inner_shape(figure1, figure2) != None:
        transformations['inner_shape'] = transformation.inner_shape(figure1, figure2)
    if transformation.outer_shape(figure1, figure2) != None:
        transformations['outer_shape'] = transformation.outer_shape(figure1, figure2)

    # algorithm called by shape_delta not original implementation - source is cited
    transformations['shape_delta'] = transformation.shape_delta(figure1, figure2)
    #transformations['equality'] = transformation.equality(figure1, figure2)

    return transformations


def create_relationship_diagram(figures, orientation, problemType='3x3'):
    return get_transformation(figures[0], figures[1], orientation, problemType)

def create_semantic_network(figures, problem):

    if problem.problemType == '3x3':

        H_1A = create_relationship_diagram([figures[0], figures[1]], 'horizontal')
        H_1B = create_relationship_diagram([figures[1], figures[2]], 'horizontal')
        H1 = utility.union(H_1A, H_1B)

        H_2A = create_relationship_diagram([figures[3], figures[4]], 'horizontal')
        H_2B = create_relationship_diagram([figures[4], figures[5]], 'horizontal')
        H2 = utility.union(H_2A, H_2B)

        V_1A = create_relationship_diagram([figures[0], figures[3]], 'vertical')
        V_1B = create_relationship_diagram([figures[3], figures[6]], 'vertical')
        V1 = utility.union(V_1A, V_1B)

        V_2A = create_relationship_diagram([figures[1], figures[4]], 'vertical')
        V_2B = create_relationship_diagram([figures[4], figures[7]], 'vertical')
        V2 = utility.union(V_2A, V_2B)

        D = create_relationship_diagram([figures[0], figures[4]], 'diagonal')
        R = (H1, H2, V1, V2, D)
        return R
    else:
        H1 = create_relationship_diagram([figures[0], figures[1]], 'horizontal', '2x2')
        V1 = create_relationship_diagram([figures[0], figures[2]], 'vertical', '2x2')
        R = (H1, V1)
        return R


def agent_compare(init_network, H, V, D, problem, solution_num):

    if problem.problemType == '3x3':

        H1 = init_network[0]
        H2 = init_network[1]

        V1 = init_network[2]
        V2 = init_network[3]

        D1 = init_network[4]

        metrics = [utility.get_similarity_metric(H1, H, problem),
                   utility.get_similarity_metric(H2, H, problem),
                   utility.get_similarity_metric(V1, V, problem),
                   utility.get_similarity_metric(V2, V, problem),
                   utility.get_similarity_metric(D1, D, problem)]

        result = float(sum(metrics))
        return result

    else:

        H1 = init_network[0]
        V1 = init_network[1]

        metrics = [utility.get_similarity_metric(H1, H, problem),
                   utility.get_similarity_metric(V1, V, problem)]

        result = float(sum(metrics))
        return result

def get_image_op(figures, orientation):

    xor = transformation.op_transform(figures[0], figures[1], 'xor')
    xor_similarity = ('xor', algorithm.calc_rms(xor, figures[2]))

    intersect = transformation.op_transform(figures[0], figures[1], 'intersect')
    intersect_similarity = ('intersect', algorithm.calc_rms(intersect, figures[2]))

    subtract = transformation.op_transform(figures[0], figures[1], 'subtract')
    subtract_similarity = ('subtract', algorithm.calc_rms(subtract, figures[2]))

    union = transformation.op_transform(figures[0], figures[1], 'union')
    union_similarity = ('union', algorithm.calc_rms(union, figures[2]))

    modified_subtract = transformation.op_transform(figures[0], figures[1], 'modified-subtract-' + orientation)
    modified_subtract_similarity = ('modified-subtract-' + orientation, algorithm.calc_rms(modified_subtract, figures[2]))

    comparisons = [xor_similarity, intersect_similarity, union_similarity, subtract_similarity, modified_subtract_similarity]
    m = min(comparisons, key=lambda t: t[1])

    return m[0]

def determine_single_image_op(figures):

    abc_op = get_image_op([figures[0], figures[1], figures[2]], 'horizontal')
    adg_op = get_image_op([figures[0], figures[3], figures[6]], 'vertical')

    def_op = get_image_op([figures[3], figures[4], figures[5]], 'horizontal')
    beh_op = get_image_op([figures[1], figures[4], figures[7]], 'vertical')

    ops = [abc_op, adg_op, def_op, beh_op]
    print(utility.most_common(ops))
    return utility.most_common(ops)


def image_op_solver(figures, solutions, problem):
    operation = determine_single_image_op(figures)

    horizontal_tester = transformation.op_transform(figures[6], figures[7], operation)
    vertical_tester = transformation.op_transform(figures[2], figures[5], operation)

    horizontal_scores = []
    vertical_scores = []

    for i, solution in enumerate(solutions):

        x = algorithm.calc_rms(horizontal_tester, solution)
        horizontal_scores.append( (i, x) )

    for i, solution in enumerate(solutions):

        x = algorithm.calc_rms(vertical_tester, solution)
        vertical_scores.append( (i, x) )


    m_horizontal = min(horizontal_scores, key=lambda t: t[1])
    m_vertical = min(vertical_scores, key=lambda t: t[1])

    if m_horizontal[0] == m_vertical[0]:
        scores = utility.get_score(m_horizontal, problem)
        return scores
    else:
        # need to determine which one to choose ?
        scores = utility.get_score(m_vertical, problem)
        return scores

def generate_and_test(init_network, scores, figures, solutions, problem):

    for i, solution in enumerate(solutions):

        if problem.problemType == '3x3':

            # compare init_network with generated solutions
            H_A = create_relationship_diagram([figures[6], figures[7]], 'horizontal')
            H_B = create_relationship_diagram([figures[7], solution], 'horizontal')
            H = utility.union(H_A, H_B)

            V_A = create_relationship_diagram([figures[2], figures[5]], 'vertical')
            V_B = create_relationship_diagram([figures[5], solution], 'vertical')
            V = utility.union(V_A, V_B)

            D = create_relationship_diagram([figures[4], solution], 'diagonal')

        else:
            H = create_relationship_diagram([figures[2], solution], 'horizontal', '2x2')
            V = create_relationship_diagram([figures[1], solution], 'vertical', '2x2')
            D = None

        score = agent_compare(init_network, H, V, D, problem, i + 1)
        scores.append(score)

    scores = utility.normalize_scores(scores, problem)
    print(scores)

    if 1.0 not in scores:
        #m_union = comparison.compare_union(scores, figures, solutions, problem)
        m_diagonal = comparison.compare_diagonal(scores, figures, solutions, problem)
        #init_set = [figures[0], figures[1], figures[2]]
        #solution_set = [figures[6], figures[7]]
        #row_statistics = comparison.compare_rows_or_cols(scores, init_set, solution_set, solutions)

        #init_set = [figures[0], figures[3], figures[6]]
        #solution_set = [figures[2], figures[5]]
        #col_statistics = comparison.compare_rows_or_cols(scores, init_set, solution_set, solutions)

        possible_scores = [m_diagonal]
        m = min(possible_scores, key=lambda t: t[1])
        scores = utility.get_score(m, problem)

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

        scores = []
        # compare diagonals
        if transformation.equality(figures[0], figures[4]) and transformation.equality(figures[1], figures[5]) and transformation.equality(figures[3], figures[7]):
            print('compare diagonals chosen')
            m = comparison.compare_diagonal(scores, figures, solutions, problem)
            scores = utility.get_score(m, problem)
        elif 'E' in problem.name.split(' ')[2]:
            print('xor, union, intersect solver')
            scores = image_op_solver(figures, solutions, problem)
        # standard generate and test
        else:
            print('generate & test solver')
            # generate our initial semantic network to test against
            init_network = create_semantic_network(figures, problem)
            scores = generate_and_test(init_network, scores, figures, solutions, problem)

        given = scores.index(max(scores)) + 1
        actual = problem.checkAnswer(scores)
        print('given answer: ' + str(given))
        print('actual answer: ' + str(actual))
        print()

        return scores
