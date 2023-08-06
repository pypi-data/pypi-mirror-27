# Copyright (c) 2017, Venkatesh-Prasad Ranganath
#
# BSD 3-clause License
#
# Author: Venkatesh-Prasad Ranganath (rvprasad)

import functools
import itertools


def funcify_return(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return funcify(func(*args, **kwargs))
    return wrapper


@funcify_return
def filter_op(self, predicate):
    """
    Identify elements of this iterable that satisfy the given predicate.
    :param self: is this iterable
    :param predicate: to be satisfied by an element
    :return: a funcified iterable of elements that satisfied the predicate
    """
    return filter(predicate, self)


@funcify_return
def map_op(self, transformer):
    """
    Transform elements of this iterable.
    :param self: is this iterable
    :param transformer: transforms an element
    :return: a funcified iterable of transformed elements
    """
    return map(transformer, self)


@funcify_return
def flat_map_op(self, transformer):
    """
    Transform elements of this iterable.  If a transformed element is an
    iterable, then these elements will appear as the elements of the result
    (instead of the iterable).
    :param self: is this iterable
    :param transformer: transforms an element
    :return: a funcified flattened iterable of transformed elements
    """
    return funcify(itertools.chain.from_iterable(map(transformer, self)))


@funcify_return
def reduce_op(self, combiner, init_val):
    """
    Reduces this iterable.
    :param self: is this iterable
    :param combiner: reduce this iterable starting with init_val
    :param init_val: is the initial value of the combination operation
    :return: the combination of elements of this iterable.  If the combination
    is an iterable, then it is funcified.
    """
    return functools.reduce(combiner, self, init_val)


@funcify_return
def foldl_op(self, combine):
    """
    Folds this iterable from left to right.
    :param self: is this iterable
    :param combiner: folds this iterable
    :return: the result of folding of this iterable.  If the result is an
    iterable, then it is funcified.
    """
    return functools.reduce(combine, self)


@funcify_return
def foldr_op(self, combine):
    """
    Folds this iterable from right to left.
    :param self: is this iterable
    :param combiner: folds this iterable
    :return: the result of folding of this iterable.  If the result is an
    iterable, then it is funcified.
    """
    obj = self
    if not hasattr(self, '__reversed__'):
        obj = list(self)
    return functools.reduce(combine, reversed(obj))


def sum_op(self):
    """
    Sums up this iterable.
    :param self: is this iterable
    :return: the sum of the elements in this iterable
    """
    return sum(self)


def count_op(self, predicate):
    """
    Counts the elements in this iterable that satisfy the given predicate.
    :param self: is this iterable
    :param predicate: to be satisfied by an element to be counted
    :return: the number of the elements that satisfy the given predicate
    """
    return sum(map(predicate, self))


def max_op(self):
    """
    Identifies the maximum element in this iterable.
    :param self: is this iterable
    :return: the maximum elements in this iterable
    """
    return max(self)


def min_op(self):
    """
    Identifies the minimum element in this iterable.
    :param self: is this iterable
    :return: the minimum elements in this iterable
    """
    return min(self)


def all_op(self):
    """
    Checks if all elements in this iterable are true.
    :param self: is this iterable
    :return: True if all elements are true; false, otherwise
    """
    return all(self)


def any_op(self):
    """
    Checks if any element in this iterable is true.
    :param self: is this iterable
    :return: True if any element is true; false, otherwise
    """
    return any(self)


@funcify_return
def zip_op(self, iterable):
    """
    Aggregates the elements of this iterable with given iterable.
    :param self: is this iterable
    :param iterable: to be aggregate with
    :return: a funcified iterable of tuples such that, in the i-th tuple,
    the first element is the i-th element in this iterable and the second
    element is the i-th element in the given iterable
    """
    return zip(self, iterable)


def __helper__(obj):
    obj.map = map_op.__get__(obj)
    obj.filter = filter_op.__get__(obj)
    obj.reduce = reduce_op.__get__(obj)
    obj.foldl = foldl_op.__get__(obj)
    obj.foldr = foldr_op.__get__(obj)
    obj.flat_map = flat_map_op.__get__(obj)
    obj.sum = sum_op.__get__(obj)
    obj.count = count_op.__get__(obj)
    obj.max = max_op.__get__(obj)
    obj.min = min_op.__get__(obj)
    obj.all = all_op.__get__(obj)
    obj.any = any_op.__get__(obj)
    obj.zip = zip_op.__get__(obj)
    return obj


class _ListWrapper(list):
    def __init__(self, obj):
        list.__init__(self, obj)
        __helper__(self)


class _SetWrapper(set):
    def __init__(self, obj):
        set.__init__(self, obj)
        __helper__(self)


class _DictWrapper(dict):
    def __init__(self, obj):
        dict.__init__(self, obj)
        __helper__(self)


class _TupleWrapper(tuple):
    def __new__(cls, value):
        return super(_TupleWrapper, cls).__new__(cls, value)

    def __init__(self, obj):
        __helper__(self)


class _StrWrapper(str):
    def __new__(cls, value):
        return super(_StrWrapper, cls).__new__(cls, value)

    def __init__(self, obj):
        __helper__(self)


class _RangeWrapper(object):
    def __init__(self, obj):
        self.range = obj
        __helper__(self)

    def __iter__(self):
        return _IterWrapper(iter(self.range))

    def __getattr__(self, x):
        return getattr(self.range, x)

    def __reversed__(self):
        return _IterWrapper(reversed(self.range))


class _IterWrapper(object):
    def __init__(self, obj):
        self.iter = obj
        __helper__(self)

    def __iter__(self):
        return self

    def __next__(self):
        return self.iter.__next__()

    def __getattr__(self, x):
        return getattr(self.iter, x)


def funcify(obj):
    if not hasattr(obj, '__iter__'):
        return obj

    if isinstance(obj, list):
        return _ListWrapper(obj)
    elif isinstance(obj, set):
        return _SetWrapper(obj)
    elif isinstance(obj, dict):
        return _DictWrapper(obj)
    elif isinstance(obj, tuple):
        return _TupleWrapper(obj)
    elif isinstance(obj, str):
        return _StrWrapper(obj)
    elif isinstance(obj, range):
        return _RangeWrapper(obj)
    elif hasattr(obj, '__dict__'):
        return __helper__(obj)
    elif hasattr(obj, '__next__'):
        return _IterWrapper(obj)
    else:
        return obj
