import math
import matplotlib.pyplot as plt
from probablity import Probablity
# Binomial probablity class


class Binomial(Probablity):
    def __init__(self, prob):
        self.probablity = prob
        pass

    def probablityofsuccess(self, n, k):
        a = self.nchoosek(n, k)
        b = self.probablity ** k
        c = (1-self.probablity) ** (n-k)

        return a*b*c

    def variance(self):
        return self.probablity*(1-self.probablity)

    def expected(self):
        return self.probablity

    def printTable(self, n):
        for k in range(n+1):
            print(k, ':', self.probablityofsuccess(n, k))

    def graph(self, n):
        plt.figure(num='Bernouli Distribution')
        plt.xlabel('Number of sucessful results')
        plt.ylabel('probability of success')
        probs = []
        ks = []
        sum = 0
        for k in range(n+1):
            #plt.plot(k, self.probablityofsuccess(n, k))
            sum += self.probablityofsuccess(n, k)
            probs.append(self.probablityofsuccess(n, k))
            ks.append(k)
            print(k, ':', self.probablityofsuccess(n, k))

        plt.plot(ks, probs)
        plt.show()


#flipCoin = Binomial(0.5)
# print(flipCoin.probablityofsuccess(5,2))
#size = 3
#print("Probablity of getting k heads after", size, "coin flips")
# flipCoin.graph(size)
