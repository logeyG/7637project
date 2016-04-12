from PIL import Image
from visual import utility
from visual import algorithm
from visual import transformation

def compare_top_corners(figures):

    a_blobs = algorithm.get_blobs(algorithm.find_regions(figures[0]))
    c_blobs = algorithm.get_blobs(algorithm.find_regions(figures[2]))

    d_blobs = algorithm.get_blobs(algorithm.find_regions(figures[3]))
    f_blobs = algorithm.get_blobs(algorithm.find_regions(figures[5]))

    if len(a_blobs) < 2 or len(c_blobs) < 2 or len(d_blobs) < 2 or len(f_blobs) < 2:
        return False

    if transformation.strict_equality(a_blobs[algorithm.get_top(a_blobs)], c_blobs[algorithm.get_top(c_blobs)]) \
        and transformation.strict_equality(d_blobs[algorithm.get_top(d_blobs)], f_blobs[algorithm.get_top(f_blobs)]):
        return True
    else:
        return False

def compare_bottom_bc_ef(figures):

    b_blobs = algorithm.get_blobs(algorithm.find_regions(figures[1]))
    c_blobs = algorithm.get_blobs(algorithm.find_regions(figures[2]))

    e_blobs = algorithm.get_blobs(algorithm.find_regions(figures[4]))
    f_blobs = algorithm.get_blobs(algorithm.find_regions(figures[5]))

    if len(b_blobs) < 2 or len(c_blobs) < 2 or len(e_blobs) < 2 or len(f_blobs) < 2:
        return False

    if transformation.strict_equality(b_blobs[algorithm.get_bottom(b_blobs)], c_blobs[algorithm.get_bottom(c_blobs)]) \
        and transformation.strict_equality(e_blobs[algorithm.get_bottom(e_blobs)], f_blobs[algorithm.get_bottom(f_blobs)]):
        return True
    else:
        return False

def compare_top_bottom(scores, figures, solutions, problem):

    if not scores:
        scores = [.125, .125, .125, .125, .125, .125, .125, .125]

    g_blobs = algorithm.get_blobs(algorithm.find_regions(figures[6]))
    h_blobs = algorithm.get_blobs(algorithm.find_regions(figures[7]))

    top_g = g_blobs[algorithm.get_top(g_blobs)]
    bottom_h = h_blobs[algorithm.get_bottom(h_blobs)]

    possible_answers = []
    for i, score in enumerate(scores):
        if score != 0.0:
            possible_answers.append( (i, solutions[i]))

    comparisons = []
    for answer in possible_answers:

        solution_blobs = algorithm.get_blobs(algorithm.find_regions(answer[1]))
        top_solution = solution_blobs[algorithm.get_top(solution_blobs)]
        bottom_solution = solution_blobs[algorithm.get_bottom(solution_blobs)]

        x = ( answer[0], algorithm.calc_rms(top_g, top_solution) + algorithm.calc_rms(bottom_h, bottom_solution))
        comparisons.append(x)

    m = min(comparisons, key=lambda t: t[1])

    return m

def compare_rows_or_cols(scores, init_set, solution_set, solutions):

    abc_pixel_count = algorithm.fill_ratio(init_set[0]) + algorithm.fill_ratio(init_set[1]) \
                      + algorithm.fill_ratio(init_set[2])

    abc_shape_count = algorithm.find_regions(init_set[0]) + algorithm.find_regions(init_set[1]) \
                        + algorithm.find_regions(init_set[2])

    gh_pixel_count = algorithm.fill_ratio(solution_set[0]) + algorithm.fill_ratio(solution_set[1])
    gh_shape_count = algorithm.find_regions(solution_set[0]) + algorithm.find_regions(solution_set[1])

    possible_answers = []
    for i, score in enumerate(scores):
        if score != 0.0:
            possible_answers.append( (i, solutions[i]))

    comparisons = []
    for answer in possible_answers:
        x = (gh_pixel_count + algorithm.fill_ratio(answer[1]), len(gh_shape_count) + len(algorithm.find_regions(answer[1])) )
        comparisons.append(x)

    x = (abc_pixel_count, len(abc_shape_count))

    closest = utility.closest_node(x, comparisons)

    return (possible_answers[closest][0], possible_answers[closest][1])


def compare_diagonal(scores, figures, solutions, problem):

    if not scores:
        scores = [.125, .125, .125, .125, .125, .125, .125, .125]

    possible_answers = []
    for i, score in enumerate(scores):
        if score != 0.0:
            possible_answers.append( (i, solutions[i]))

    comparisons = []
    for answer in possible_answers:
        x = ( answer[0], algorithm.calc_rms(figures[4], answer[1]))
        comparisons.append(x)

    m = min(comparisons, key=lambda t: t[1])

    return m

def compare_union(scores, figures, solutions, problem):

    comparisons = []
    for i, score in enumerate(scores):

        if score != 0.0:

            if problem.problemType == '3x3':
                merged = utility.image_union(figures[5], figures[7])
                solution = Image.open(solutions[i].visualFilename)
                x = (i, algorithm.calc_rms(merged, solution))
            else:
                merged = utility.image_union(figures[1], figures[2])
                solution = Image.open(solutions[i].visualFilename)
                x = (i, algorithm.calc_rms(merged, solution))
            comparisons.append(x)

    m = min(comparisons, key=lambda t: t[1])

    return m
