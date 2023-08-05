# coding=UTF-8
from __future__ import print_function, absolute_import, division

import copy
import functools
import heapq
import logging

import six

from .typecheck import typed, Callable, Iterable

logger = logging.getLogger(__name__)

__all__ = [
    'CallableGroup',
    'Heap',
    'TimeBasedHeap'
]

returns_bool = typed(returns=bool)
returns_iterable = typed(returns=Iterable)


class CallableGroup(object):
    """
    This behaves like a function, but allows to add other functions to call
    when invoked, eg.

        c1 = Callable()

        c1.add(foo)
        c1.add(bar)

        c1(2, 3)

    Now both foo and bar will be called with arguments (2, 3). Their exceptions
    will be propagated.

    """

    # todo not threadsafe with oneshots

    def __init__(self, gather=False, swallow_exceptions=False):
        """
        :param gather: if True, results from all callables will be gathered
                       into a list and returned from __call__
        :param swallow_exceptions: if True, exceptions from callables will be
                                   silently ignored. If gather is set,
                                   result will be the exception instance
        """
        self.callables = []  # tuple of (callable, oneshot)
        self.gather = gather
        self.swallow_exceptions = swallow_exceptions

    @typed(None, Callable, bool)
    def add(self, callable, oneshot=False):
        """
        :param oneshot: if True, callable will be unregistered after single call
        """
        self.callables.append((callable, oneshot))

    def __call__(self, *args, **kwargs):
        """
        Run the callable. All registered callables will be called with
        passed arguments, so they should have the same arity.

        If callables raise, it will be passed through.

        :return: list of results if gather was set, else None
        """
        clbl = self.callables  # for moar thread safety
        self.callables = []

        if self.gather:
            results = []

        for callable, oneshot in clbl:
            try:
                q = callable(*args, **kwargs)
            except Exception as e:
                if not self.swallow_exceptions:
                    raise  # re-raise
                q = e

            if self.gather:
                results.append(q)

            if not oneshot:
                self.callables.append((callable, oneshot))

        if self.gather:
            return results


def _extras_to_one(fun):
    @functools.wraps(fun)
    def inner(self, a, *args, **kwargs):
        return fun(self, ((a,) + args) if len(args) > 0 else a, **kwargs)

    return inner


class Heap(object):
    """
    Sane heap as object - not like heapq.

    Goes from lowest-to-highest (first popped is smallest).
    Standard Python comparision rules apply.

    Not thread-safe
    """

    __slots__ = ('heap',)  # this is rather private, plz

    def __init__(self, from_list=()):
        self.heap = list(from_list)
        heapq.heapify(self.heap)

    @typed(object, Iterable)
    def push_many(self, items):
        for item in items:
            self.push(item)

    # TODO needs tests
    @_extras_to_one
    def push(self, item):
        """
        Use it like:

            heap.push(3)

        or:

            heap.push(4, myobject)
        """
        heapq.heappush(self.heap, item)

    def __copie(self, op):
        h = Heap()
        h.heap = op(self.heap)
        return h

    def __deepcopy__(self, memo):
        return self.__copie(copy.deepcopy)

    def __copy__(self):
        return self.__copie(copy.copy)

    def __iter__(self):
        return self.heap.__iter__()

    def pop(self):
        """
        Return smallest element of the heap.
        :raises IndexError: on empty heap
        """
        return heapq.heappop(self.heap)

    @typed(object, (Callable, None), (Callable, None))
    def filtermap(self, filter_fun=None, map_fun=None):
        """
        Get only items that return True when condition(item) is True. Apply a
         transform: item' = item(condition) on
        the rest. Maintain heap invariant.
        """
        heap = filter(filter_fun, self.heap) if filter_fun else self.heap
        heap = map(map_fun, heap) if map_fun else heap
        heap = list(heap) if not isinstance(heap, list) else heap
        self.heap = heap
        heapq.heapify(self.heap)

    @returns_bool
    def __bool__(self):
        """
        Is this empty?
        """
        return len(self.heap) > 0

    @returns_iterable
    def iter_ascending(self):
        """
        Return an iterator returning all elements in this heap sorted ascending.
        State of the heap is not changed
        :return: Iterator
        """
        heap = copy.copy(self.heap)
        while heap:
            yield heapq.heappop(heap)

    @returns_iterable
    def iter_descending(self):
        """
        Return an iterator returning all elements in this heap sorted descending.
        State of the heap is not changed
        :return: Iterator
        """
        return reversed(list(self.iter_ascending()))

    @typed(returns=six.integer_types)
    def __len__(self):
        return len(self.heap)

    def __str__(self):
        return '<satella.coding.Heap: %s elements>' % (len(self.heap, ))

    def __unicode__(self):
        return six.text_type(str(self))

    def __repr__(self):
        return u'<satella.coding.Heap>'

    @returns_bool
    def __contains__(self, item):
        return item in self.heap


class TimeBasedHeap(Heap):
    """
    A heap of items sorted by timestamps.

    It is easy to ask for items, whose timestamps are LOWER than a value, and
    easy to remove them.

    Can be used to implement a scheduling service, ie. store jobs, and each
    interval query
    which of them should be executed. This loses time resolution, but is fast.

    Can use current time with put/pop_less_than.
    Use default_clock_source to pass a callable:

      * time.time
      * monotonic.monotonic

    #notthreadsafe
    """

    def __repr__(self):
        return u'<satella.coding.TimeBasedHeap>'

    @returns_iterable
    def items(self):
        """
        Return an iterator, but WITHOUT timestamps (only items), in
        unspecified order
        """
        return (ob for ts, ob in self.heap)

    def __init__(self, default_clock_source=lambda: None):
        """
        Initialize an empty heap
        """
        self.default_clock_source = default_clock_source
        super(TimeBasedHeap, self).__init__()

    def put(self, *args):
        """
        Put an item of heap.

        Pass timestamp, item or just an item for default time
        """
        assert len(args) in (1, 2)

        if len(args) == 1:
            timestamp, item = self.default_clock_source(), args[0]
        else:
            timestamp, item = args

        assert timestamp is not None
        self.push((timestamp, item))

    @returns_iterable
    def pop_less_than(self, less=None):
        """
        Return all elements less (sharp inequality) than particular value.

        This changes state of the heap
        :param less: value to compare against
        :return: Iterator
        """

        if less is None:
            less = self.default_clock_source()

        assert less is not None

        while self:
            if self.heap[0][0] >= less:
                return
            yield self.pop()

    def remove(self, item):
        """
        Remove all things equal to item
        """
        self.filtermap(filter_fun=lambda i: i != item)
