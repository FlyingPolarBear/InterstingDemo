import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def Birthday(d):
    a = np.zeros(100)
    for n in range(100):
        a[n] = 1-np.exp(-n*(n-1)/(2*d))
        print("d=%d," % d, "n=%d, " % n, "possibility: ", a[n])
    plt.plot(a,label='d='+str(d))


for d in range(100, 1000, 100):
    Birthday(d)
plt.xlabel('N number')
plt.ylabel('Possibility')
plt.legend()
plt.show()
