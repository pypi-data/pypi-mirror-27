from math import inf


class HandGrenade(dict):
    def __contains__(self, item):
        return self and self.lower <= item <= self.upper

    def __delitem__(self, key):
        super().__delitem__(key)
        self._generate_tree()

    def __eq__(self, other):
        return (isinstance(other, HandGrenade)
                and super().__eq__(other)
                and self.lower == other.lower
                and self.upper == other.upper)

    def __getitem__(self, item):
        current = self._tree
        while current:
            if item < current.lower:
                current = current.before
            elif item > current.upper:
                current = current.after
            else:
                return current.value
        raise KeyError(item)

    def __init__(self, *args, lower=-inf, upper=inf, **kwargs):
        super().__init__(*args, **kwargs)
        self.lower = lower
        self.upper = upper
        self._tree = None
        if lower > upper:
            raise ValueError('Lower cannot be greater than upper')
        for key in self.keys():
            if key < lower or key > upper:
                raise KeyError(key)
        self._generate_tree()

    def __ne__(self, other):
        return (not isinstance(other, HandGrenade)
                or super().__ne__(other)
                or self.lower != other.lower
                or self.upper != other.upper)

    def __repr__(self):
        return '{name}({dict_repr}, lower={lower}, upper={upper})'.format(
            name=HandGrenade.__name__,
            dict_repr=super().__repr__(),
            lower=self.lower,
            upper=self.upper
        )

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._generate_tree()

    def _generate_tree(self):
        range_mapping = [(((p + c) / 2, (c + n) / 2), dict.get(self, c))
                         for p, c, n in self._iterate_keys()]
        # Use iterative solution instead of recursive
        if range_mapping:
            self._tree = HandGrenade.Node()
            stack = [(self._tree, range_mapping)]
            while stack:
                node, ranges = stack.pop()
                children = node.init(ranges)
                stack.extend(children)
        else:
            self._tree = None

    def _iterate_keys(self):
        if self:
            keys = sorted(self.keys())
            lower, upper = 2 * self.lower - keys[0], 2 * self.upper - keys[-1]
            result = zip([lower] + keys[:-1], keys, keys[1:] + [upper])
        else:
            result = zip()
        return result

    def clear(self):
        super().clear()
        self._tree = None

    def copy(self):
        return HandGrenade(super().copy())

    def pop(self, *args, **kwargs):
        value = super().pop(*args, **kwargs)
        self._generate_tree()
        return value

    def popitem(self):
        value = super().popitem()
        self._generate_tree()
        return value

    def setdefault(self, key, *args, **kwargs):
        if key < self.lower or key > self.upper:
            raise KeyError(key)
        value = super().setdefault(key, *args, **kwargs)
        self._generate_tree()
        return value

    def update(self, dictionary):
        for key in dictionary:
            if key < self.lower or key > self.upper:
                raise KeyError(key)
        for key, value in dictionary.items():
            self[key] = value
        self._generate_tree()

    class Node:
        def __init__(self):
            self.value = None
            self.lower = None
            self.upper = None
            self.before = None
            self.after = None

        def init(self, range_mapping):
            children = []
            middle = len(range_mapping) // 2
            (self.lower, self.upper), self.value = range_mapping[middle]
            before, after = range_mapping[:middle], range_mapping[middle + 1:]
            if before:
                self.before = HandGrenade.Node()
                children.append((self.before, before))
            if after:
                self.after = HandGrenade.Node()
                children.append((self.after, after))
            return children
