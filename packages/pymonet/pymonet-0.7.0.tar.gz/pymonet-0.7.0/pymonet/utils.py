from functools import reduce


def identity(value):
    return value


def increase(value):
    return value + 1


def eq(value, *args):
    if args:
        return value == args[0]
    return lambda other: value == other


def curried_map(mapper):
    return lambda collection: [mapper(item) for item in collection]


def curried_filter(filterer):
    return lambda collection: [item for item in collection if filterer(item)]


def find(collection, key):
    """
    Returns the first element of the list which matches the keys, or None if no element matches.
    :param collection
    :type List<A>
    :param key: function to decide witch element should be found
    :type (A) -> Boolean
    :return element of collection or None
    :type A | None
    """
    for item in collection:
        if key(item):
            return item


def compose(value, *functions):
    """
    Performs right-to-left function composition.
    :param value - argument of first applied function
    :type Any
    :param functions - list of functions to applied from right-to-left
    :return result of all functions
    :typa Any
    """
    return reduce(
        lambda current_value, function: function(current_value),
        functions[::-1],
        value
    )


def pipe(value, *functions):
    """
    Performs left-to-right function composition.
    :param value - argument of first applied function
    :type Any
    :param functions - list of functions to applied from ledt-to-right
    :return result of all functions
    :typa Any
    """
    return reduce(
        lambda current_value, function: function(current_value),
        functions,
        value
    )


def cond(condition_list):
    """
    Function for return function depended on first function argument
    cond get list of two-item tuples,
    first is condition_function, second is execute_function.
    Returns this execute_function witch first condition_function return truly value
    :param condition_list: list of two-item tuples (condition_function, execute_function)
    :type List<(Function, Function)>
    :return Returns this execute_function witch first condition_function return truly value
    :type Function
    """
    def result(*args):
        for (condition_function, execute_function) in condition_list:
            if condition_function(*args):
                return execute_function(*args)

    return result


def memoize(fn, key=eq):
    """
    Creates a new function that, when invoked,
    caches the result of calling fn for a given argument set and returns the result.
    Subsequent calls to the memoized fn with the same argument set will not result in an additional call to fn;
    instead, the cached result for that set of arguments will be returned.
    :param fn: function to invoke
    :type (A) -> B
    :key function to decide if result should be taken from cache
    :type (A, A) -> Boolean
    :return new function invoking old one
    :type (A) -> B
    """
    cache = []

    def memoized_fn(argument):
        cached_result = find(cache, lambda cacheItem: key(cacheItem[0], argument))
        if cached_result is not None:
            return cached_result[1]
        fn_result = fn(argument)
        cache.append((argument, fn_result))
        return fn_result

    return memoized_fn
