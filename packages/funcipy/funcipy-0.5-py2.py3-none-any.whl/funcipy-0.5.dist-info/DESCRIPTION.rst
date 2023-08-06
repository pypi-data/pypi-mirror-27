funcipy
=======

A library to inject common functional programming operations as methods
into iterable objects. Currently, it injects
``filter, flat_map, foldl, foldr, map,`` and ``reduce`` operations along
with ``sum, count, any, all, max, min,`` and ``zip`` operations.

Getting the library
-------------------

The library can be installed via ``pip install funcipy``. Similarly, it
can be uninstalled via ``pip uninstall funcipy``.

Usage
-----

When you want to inject common functional programming operations as
methods into an object *Obj*, invoke ``funcipy.funcify`` function with
*Obj* as the argument. If *Obj* is iterable, then the function will
return an object that

1. provides the same interface as the input object and
2. has functional programming operations as methods.

Otherwise, *Obj* is returned as is.

Here are few example invocations.

.. code:: python

    from funcipy import funcify
    import functools
    import itertools
    import operator

    i = range(5, 15)
    print("Map function: " + ' '.join(map(str, i)))
    tmp1 = funcify(i)
    print("Map function applied to funcified object: " + ' '.join(map(str, tmp1)))
    print("Map method: " + ' '.join(tmp1.map(str)))
    print("Map and Filter Method chaining: " +
          ' '.join(tmp1.filter(lambda x: x % 2).map(str)))

    print("Reduce function: " + str(functools.reduce(operator.add, i, 5)))
    print("Reduce method: " + str(tmp1.reduce(operator.add, 5)))
    print("Reduce function: " + str(functools.reduce(operator.sub, i)))
    print("Foldl method: " + str(tmp1.foldl(operator.sub)))
    print("Foldr method: " + str(tmp1.foldr(operator.sub)))
    print("Flat-map operation: " + ' '.join(itertools.chain.from_iterable(
        map(str, i))))
    print("Flat-map method: " + ' '.join(funcify(i).flat_map(str)))
    print("Sum function: " + str(sum(i)))
    print("Sum method: " + str(tmp1.sum()))
    print("Count function: " + str(sum(1 for _ in filter(lambda x: x > 10, i))))
    print("Count method: " + str(tmp1.count(lambda x: x > 10)))
    print("Max function: " + str(max(i)))
    print("Max method: " + str(tmp1.max()))
    print("Min function: " + str(min(i)))
    print("Min method: " + str(tmp1.min()))
    print("Any function: " + str(any(map(lambda x: x > 10, i))))
    print("Any method: " + str(tmp1.map(lambda x: x > 10).any()))
    print("All function: " + str(all(map(lambda x: x > 10, i))))
    print("All method: " + str(tmp1.map(lambda x: x > 10).all()))
    j = range(0, 7)
    print("Zip function: " + ' '.join(map(str, zip(i, j))))
    print("Zip method: " + ' '.join(tmp1.zip(j).map(str)))

Attribution
-----------

Copyright (c) 2017, Venkatesh-Prasad Ranganath

Licensed under BSD 3-clause "New" or "Revised" License
(https://choosealicense.com/licenses/bsd-3-clause/)

**Authors:** Venkatesh-Prasad Ranganath


