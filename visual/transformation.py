from visual import algorithm
from PIL import Image
from PIL import ImageChops
from visual import utility

def equality(source, compare):

    if round(algorithm.calc_rms(source, compare), 0) < 970.0:
        return True
    else:
        return False

def strict_equality(source, compare):

    if round(algorithm.calc_rms(source, compare), 0) < 960.0:
        return True
    else:
        return False

def op_transform(im1, im2, operation):

    source, compare = utility.open_image(im1, im2)

    if operation == 'xor':
        x = algorithm.xor(source, compare)
        return x
    elif operation == 'union':
        x = ImageChops.multiply(source, compare)
        return x
    elif operation == 'subtract':
        x = algorithm.subtract(source, compare)
        return x
    elif operation == 'intersect':
        x = algorithm.intersect(source, compare)
        return x
    elif operation == 'modified-subtract-horizontal':
        x = algorithm.modified_subtract(source, compare, 'horizontal')
        return x
    elif operation == 'modified-subtract-vertical':
        x = algorithm.modified_subtract(source, compare, 'vertical')
        return x

def outer_shape(source, compare):

    source_blobs = algorithm.get_blobs(algorithm.find_regions(source))
    compare_blobs = algorithm.get_blobs(algorithm.find_regions(compare))

    if len(source_blobs) < 2 or len(compare_blobs) < 2:
        return None
    else:
        source_inner = algorithm.get_center(source_blobs)
        compare_inner = algorithm.get_center(compare_blobs)

        source_blobs.pop(source_inner)
        compare_blobs.pop(compare_inner)

        source_outer = algorithm.write_blobs(source_blobs)
        compare_outer = algorithm.write_blobs(compare_blobs)

        return equality(source_outer, compare_outer)

def inner_shape(source, compare):

    source_blobs = algorithm.get_blobs(algorithm.find_regions(source))
    compare_blobs = algorithm.get_blobs(algorithm.find_regions(compare))

    source_inner = source_blobs[algorithm.get_center(source_blobs)]
    compare_inner = compare_blobs[algorithm.get_center(compare_blobs)]

    return equality(source_inner, compare_inner)

def size_comparison(source, compare):

    source_size = algorithm.find_image_size(source)
    compare_size = algorithm.find_image_size(compare)

    if compare_size > source_size and (compare_size - source_size) > 1000:
        return 'expanded'
    elif source_size > compare_size and (source_size - compare_size) > 1000:
        return 'contracted'
    else:
        return 'unchanged'

def fill_delta(source, compare):

    source_count = algorithm.fill_ratio(source)
    compare_count = algorithm.fill_ratio(compare)

    if source_count < compare_count and (compare_count - source_count) > 1500:
        return 'added'
    elif source_count > compare_count and (source_count - compare_count) > 1500:
        return 'removed'
    else:
        return 'unchanged'

def shape_delta(source, compare):

    source_count = len(algorithm.find_regions(source))
    compare_count = len(algorithm.find_regions(compare))

    if source_count < compare_count:
        return 'added'  # + str(compare_count - source_count)
    elif source_count > compare_count:
        return 'removed'  # + str(source_count - compare_count)
    else:
        return 'unchanged'