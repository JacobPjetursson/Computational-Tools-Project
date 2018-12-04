import math

n = 20000
fpr = 0.001
m = (n * abs(math.log(fpr))) / (math.log(2) ** 2)
k = (m / n) * math.log(2)

print(math.ceil(m))
print(math.ceil(k))
