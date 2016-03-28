from PIL import Image
from visual import utility
from visual import transformation

def compare_corners(scores, figures, solutions, problem):

    if not scores:
        scores = [.125, .125, .125, .125, .125, .125, .125, .125]

    possible_answers = []
    for i, score in enumerate(scores):
        if score != 0.0:
            possible_answers.append( (i, solutions[i]))

    comparisons = []
    for answer in possible_answers:
        x = ( answer[0], utility.similarity(figures[0], answer[1]))
        comparisons.append(x)

    m = min(comparisons, key=lambda t: t[1])

    if problem.problemType == '3x3':
        scores = [0, 0, 0, 0, 0, 0, 0, 0]
    else:
        scores = [0, 0, 0, 0, 0, 0]

    scores[m[0]] = 1

    return scores

def compare_diagonal(scores, figures, solutions, problem):

    if not scores:
        scores = [.125, .125, .125, .125, .125, .125, .125, .125]

    possible_answers = []
    for i, score in enumerate(scores):
        if score != 0.0:
            possible_answers.append( (i, solutions[i]))

    comparisons = []
    for answer in possible_answers:
        x = ( answer[0], utility.similarity(figures[4], answer[1]))
        comparisons.append(x)

    m = min(comparisons, key=lambda t: t[1])

    if problem.problemType == '3x3':
        scores = [0, 0, 0, 0, 0, 0, 0, 0]
    else:
        scores = [0, 0, 0, 0, 0, 0]

    scores[m[0]] = 1

    return scores

def compare_union(scores, figures, solutions, problem):

    comparisons = []
    for i, score in enumerate(scores):

        if score != 0.0:

            if problem.problemType == '3x3':
                merged = utility.image_union(figures[5], figures[7])
                solution = Image.open(solutions[i].visualFilename)
                x = (i, utility.similarity(merged, solution))
            else:
                merged = utility.image_union(figures[1], figures[2])
                solution = Image.open(solutions[i].visualFilename)
                x = (i, utility.similarity(merged, solution))
            comparisons.append(x)

    m = min(comparisons, key=lambda t: t[1])

    if problem.problemType == '3x3':
        scores = [0, 0, 0, 0, 0, 0, 0, 0]
    else:
        scores = [0, 0, 0, 0, 0, 0]

    scores[m[0]] = 1

    return scores

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