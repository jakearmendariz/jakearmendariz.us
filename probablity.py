import math


class Probablity:
    def __init__(self):
        pass

    def nchoosek(self, n, k):
        return math.factorial(n)/(math.factorial(n-k)*math.factorial(k))

    def permutations(self, n, k):
        return math.factorial(n)/math.factorial(n-k)
