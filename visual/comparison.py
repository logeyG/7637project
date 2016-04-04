from PIL import Image
from visual import utility
from visual import transformation
from visual import algorithm

def compare_corners(scores, figures, solutions, problem):

    if not scores:
        scores = [.125, .125, .125, .125, .125, .125, .125, .125]

    possible_answers = []
    for i, score in enumerate(scores):
        if score != 0.0:
            possible_answers.append( (i, solutions[i]))

    comparisons = []
    for answer in possible_answers:
        x = ( answer[0], algorithm.calc_rms(figures[0], answer[1]) )
        comparisons.append(x)

    m = min(comparisons, key=lambda t: t[1])

    return m

def compare_rows(scores, figures, solutions, problem):

    abc_pixel_count = algorithm.fill_ratio(figures[0]) + algorithm.fill_ratio(figures[1]) \
                      + algorithm.fill_ratio(figures[2])

    abc_shape_count = algorithm.find_regions(figures[0]) + algorithm.find_regions(figures[1]) \
                        + algorithm.find_regions(figures[2])

    gh_pixel_count = algorithm.fill_ratio(figures[6]) + algorithm.fill_ratio(figures[7])
    gh_shape_count = algorithm.find_regions(figures[6]) + algorithm.find_regions(figures[7])

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

def compare_reflected(scores, figures, solutions, problem):

    if not scores:
        scores = [.125, .125, .125, .125, .125, .125, .125, .125]

    for i, score in enumerate(scores):

        if score != 0.0:
            reflected_test = transformation.reflected_within_single(figures[6], solutions[i])

            if reflected_test == (True, True):
                if problem.problemType == '3x3':
                    scores = [0, 0, 0, 0, 0, 0, 0, 0]
                else:
                    scores = [0, 0, 0, 0, 0, 0]

                scores[i] = 1
                return scores

    return scores