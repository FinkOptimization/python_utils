def first(iterable, key=lambda x: True, default=None):
    for element in iterable:
        if key(element):
            return element
    return default


def get_min_element(iterable, key=lambda x: x):
    min_element = first(iterable)
    for element in iterable:
        if key(element) < key(min_element):
            min_element = element
    return min_element
