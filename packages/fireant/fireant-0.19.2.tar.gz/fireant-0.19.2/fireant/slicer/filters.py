# coding: utf8
from fireant import utils


class Filter(object):
    def __init__(self, element_key):
        self.element_key = element_key


class EqualityFilter(Filter):
    def __init__(self, element_key, operator, value):
        super(EqualityFilter, self).__init__(element_key)
        self.operator = operator
        self.value = value

    def schemas(self, elements, **kwargs):
        elements = utils.wrap_list(elements)
        value = utils.wrap_list(self.value)

        criterion = None
        for element, value in zip(elements, value):
            crit = getattr(element, self.operator)(value)
            if criterion:
                criterion = criterion & crit
            else:
                criterion = crit

        return criterion

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.element_key == other.element_key \
               and self.operator == other.operator \
               and self.value == other.value


class BooleanFilter(Filter):
    def __init__(self, element_key, value):
        super(BooleanFilter, self).__init__(element_key)
        self.value = value

    def schemas(self, element):
        if not self.value:
            return element.negate()
        return element


class ContainsFilter(Filter):
    def __init__(self, element_key, values):
        super(ContainsFilter, self).__init__(element_key)
        self.values = values

    def schemas(self, element):
        return element.isin(self.values)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.element_key == other.element_key \
               and self.values == other.values


class ExcludesFilter(Filter):
    def __init__(self, element_key, values):
        super(ExcludesFilter, self).__init__(element_key)
        self.values = values

    def schemas(self, element):
        return element.notin(self.values)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.element_key == other.element_key \
               and self.values == other.values


class RangeFilter(Filter):
    def __init__(self, element_key, start, stop):
        super(RangeFilter, self).__init__(element_key)
        self.start = start
        self.stop = stop

    def schemas(self, element):
        element = utils.wrap_list(element)
        starts = utils.wrap_list(self.start)
        stops = utils.wrap_list(self.stop)

        criterion = None
        for el, start, stop in zip(element, starts, stops):
            crit = el[start:stop]
            if criterion:
                criterion = criterion & crit
            else:
                criterion = crit

        return criterion

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.element_key == other.element_key \
               and self.start == other.start \
               and self.stop == other.stop


class WildcardFilter(Filter):
    def __init__(self, element_key, value):
        super(WildcardFilter, self).__init__(element_key)
        self.value = value

    def schemas(self, element):
        return element.like(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.element_key == other.element_key \
               and self.value == other.value
