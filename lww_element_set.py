import time
from itertools import groupby


class LwwElementSet:
    """An implementation of a CvRDT Last-Write-Wins Element Set. 
        The set only accepts String elements."""

    def __init__(self, add_set=None, remove_set=None):
        if add_set is None:
            add_set = set()
        if remove_set is None:
            remove_set = set()

        self.add_set = add_set
        self.remove_set = remove_set

    def add(self, item):
        """Add an element to the set, let the timestamp be assigned automatically"""

        self.add_ts(item, time.time())

    def add_ts(self, item, ts):
        """Add an element to the set, specifying timestamp"""

        self.add_set.add((item, ts))
        self.resolve_add()

    def remove(self, item):
        """Remove an element from the set, let the timestamp be assigned automatically"""

        self.remove_ts(item, time.time())

    def remove_ts(self, item, ts):
        """Remove and element from the set, specifying timestamp"""

        self.remove_set.add((item, ts))
        self.resolve_remove()

    def merge(self, b):
        """Merge another set into this set"""
        self.add_set = self.add_set.union(b.add_set)
        self.remove_set = self.remove_set.union(b.remove_set)

        self.resolve_add()
        self.resolve_remove()

    def resolve_add(self):
        """In add_set, remove all duplicate instances of an element,
            leaving only the tuple with the latest timestamp"""
        self.add_set = set(max(g) for _, g in groupby(
            sorted(self.add_set), lambda x: x[0]))

    def resolve_remove(self):
        """In remove_set, remove all duplicate instances of an element,
            leaving only the tuple with the latest timestamp"""
        self.remove_set = set(max(g) for _, g in groupby(
            sorted(self.remove_set), lambda x: x[0]))

    def get_final_set(self):
        """Determine what the final set is by doing add/remove in the order they were done"""
        final_set = set()
        aset = set([(elem, ts, 'a') for elem, ts in self.add_set])
        rset = set([(elem, ts, 'r') for elem, ts in self.remove_set])
        temp = sorted(aset.union(rset), key=lambda x: x[1])
        for t in temp:
            if t[2] == 'a':
                final_set.add(t[0])
            else:
                final_set.discard(t[0])

        return final_set

    def __str__(self):
        """String representation of this class"""
        return '\nAdd set: {}\nRemove set: {}\nResolved: {}\n'.format(
            self.add_set, self.remove_set, self.get_final_set())

    def __eq__(self, other):
        """Overrides default implementation"""
        if isinstance(self, other.__class__):
            return (self.get_final_set() == other.get_final_set() and
                self.add_set == other.add_set and
                self.remove_set == other.remove_set)
