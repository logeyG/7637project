from PIL import Image
from PIL import ImageChops
import numpy as np

def dict_compare(d1, d2):

    # solution from
    # http://stackoverflow.com/questions/4527942/comparing-two-dictionaries-in-python
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same

def union(diagram1, diagram2):

    added, removed, modified, same = dict_compare(diagram1, diagram2)
    dic_union = {}

    for key in same:
        dic_union[key] = diagram1[key]

    return dic_union

def get_similarity_metric(a, b, problem):

    if problem.problemType == '3x3':
        added, removed, modified, same = dict_compare(a, b)
        return weighted_score(same)
    else:
        added, removed, modified, same = dict_compare(a, b)
        return weighted_score(same)

def weighted_score(same):

    score = 0
    for key in same:

        score += 1

    return score

def image_union(figure1, figure2):

    image1 = Image.open(figure1.visualFilename)
    image2 = Image.open(figure2.visualFilename)
    blended = ImageChops.darker(image1, image2)

    return blended

def get_score(m, problem):

    if problem.problemType == '3x3':
        scores = [0, 0, 0, 0, 0, 0, 0, 0]
        scores[m[0]] = 1
    else:
        scores = [0, 0, 0, 0, 0, 0]
        scores[m[0]] = 1

    return scores

def normalize_scores(scores, problem):

    if sum(scores) == 0 and problem.problemType == '3x3':
        out = [.125, .125, .125, .125, .125, .125, .125, .125]
    elif sum(scores) == 0 and problem.problemType == '2x2':
        out = [.16, .16, .16, .16, .16, .16]
    else:
        m_score = max(scores)
        for i, score in enumerate(scores):
            if score != m_score:
                scores[i] = 0

        t = float(sum(scores))
        out = [x / t for x in scores]

    return out

def open_image(im1, im2):

    if hasattr(im1, 'visualFilename'):
        source = Image.open(im1.visualFilename)
    else:
        source = im1
    if hasattr(im2, 'visualFilename'):
        compare = Image.open(im2.visualFilename)
    else:
        compare = im2

    return source, compare

def convert_to_easy_array(pixels):

    nodes = []
    for x in range(184):
        for y in range(184):
            if pixels[x, y] == (0, 0, 0, 255):  # black pixel
                nodes.append((x, y))

    return nodes

def closest_node(node, nodes):

    # http://codereview.stackexchange.com/questions/
    # 28207/finding-the-closest-point-to-a-list-of-points
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node)**2, axis=1)
    return np.argmin(dist_2)

def most_common(lst):
    return max(set(lst), key=lst.count)