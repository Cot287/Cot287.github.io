from Crypto.Util.number import *
from random import *
from tqdm import *
import matplotlib.pyplot as plt

p = getPrime(64)
q = getPrime(64)
phi = (p - 1) * (q - 1)

tot = 10**5
y = []
x = []
for dbits in trange(10, 64, 2):
    x.append(dbits)
    cnt = 0
    for t in range(10):
        for _ in range(tot):
            while 1:
                try:
                    d1 = getrandbits(dbits)
                    d2 = getrandbits(dbits)
                    e1 = inverse(d1, phi)
                    e2 = inverse(d2, phi)
                    k1 = (e1*d1 - 1) // phi
                    k2 = (e2*d2 - 1) // phi
                    if GCD(k1*d2, k2*d1) == 1:
                        cnt += 1
                    break
                except:continue
    y.append(cnt/tot/10)

# 绘制折线图
plt.figure(figsize=(10, 6))  # 设置图形大小
plt.plot(x, y, marker='o')  # 将字符串转换为浮点数，并绘制折线图
plt.title('Probability of GCD(k1*d2, k2*d1) == 1')  # 设置标题
plt.xlabel('Number of bits (dbits)')  # 设置x轴标签
plt.ylabel('Probability')  # 设置y轴标签
plt.grid(True)  # 显示网格
plt.show()  # 显示图形