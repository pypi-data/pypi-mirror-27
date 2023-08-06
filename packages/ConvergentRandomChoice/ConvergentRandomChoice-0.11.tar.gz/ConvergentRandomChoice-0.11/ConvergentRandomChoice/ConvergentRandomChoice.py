from numpy.random import choice
from math import isclose


class ConvergentRandomChoice:
    def __init__(self, iterable, pchange='uniform', initials=None):
        flag = False
        if type(pchange) != str or type(
                pchange) != float or type(pchange) != int:
            flag = True
        elif type(pchange) == str and pchange != 'uniform':
            flag = True
        elif type(pchange) == float and (pchange < 0 or pchange > 1):
            flag = True
        elif type(pchange) == int and not (pchange == 0 or pchange == 1):
            flag = True
        if flag:
            raise ValueError(
                "pchange must be a float value between 0 and 1 or 'uniform'")

        if initials and (
            len(initials) != len(iterable) or not isclose(
                sum(initials),
                1)):
            raise ValueError(
                "Error with initial probabilities, either the correct number of values is not passed in or probabilities do not sum to 1.")

        denom = 1. / len(iterable)
        if pchange == "uniform":
            self.pchange = denom
        else:
            self.pchange = pchange

        if not initials:
            self.lookup = {x: denom for x in iterable}
        else:
            self.lookup = {x: v for x, v in zip(iterable, initials)}

        self.keys = list(self.lookup.keys())
        self.len = float(len(self.lookup))

    def choice(self, num=1):
        if num < 1:
            raise ValueError("Must be a non-negative, non-zero number.")
        results = []
        for _ in range(num):
            result = choice(self.keys, 1, list(self.lookup.values()))[0]
            reduction = self.lookup[result] * self.pchange
            individual_reduction = reduction / (self.len - 1.)
            for cur in self.lookup:
                if cur != result:
                    self.lookup[cur] += individual_reduction
                else:
                    self.lookup[cur] -= reduction
            results.append(result)
        return results

    def __repr__(self):
        nl = "\n"
        tb = "\t"
        return f"Decay: {self.pchange}{nl}Items:{nl}{nl.join(tb + str(k) + ' : ' + str(v) for k, v in self.lookup.items())}"
