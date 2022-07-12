import math
import random

#0.基本运算

    #求最大公因子
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

    #求乘法逆元
def Extended_Euclidean(a, m):
    if gcd(a, m) != 1 and gcd(a, m) != -1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    if u1 > 0:
        return u1 % m
    else:
        return (u1 + m) % m

    #椭圆曲线上的点的加法
def Add(m, n):
    if (m == 0):
        return n
    if (n == 0):
        return m
    he = []
    if (m != n):
        if (gcd(m[0] - n[0], p) != 1 and gcd(m[0] - n[0], p) != -1):
            return 0
        else:
            k = ((m[1] - n[1]) * Extended_Euclidean(m[0] - n[0], p)) % p
    else:
        k = ((3 * (m[0] ** 2) + a) * Extended_Euclidean(2 * m[1], p)) % p
    x = (k ** 2 - m[0] - n[0]) % p
    y = (k * (m[0] - x) - m[1]) % p
    he.append(x)
    he.append(y)
    return he

    #椭圆曲线上的点的数乘
def Multiply(n, l):
    if n == 0:
        return 0
    if n == 1:
        return l
    t = l
    while (n >= 2):
        t = Add(t, l)
        n = n - 1
    return t

#1.ECDSA签名
def ECDSA_Sign(m, n, G, d,k):
    e = hash(m)
    R = Multiply(k, G)
    r = R[0] % n
    s = (Extended_Euclidean(k, n) * (e + d * r)) % n
    return r, s

#2.ECDSA验证
def ECDSA_Verify(m, n, G, r, s, P):
    e = hash(m)
    w = Extended_Euclidean(s, n)
    v1 = (e * w) % n
    v2 = (r * w) % n
    w = Add(Multiply(v1, G), Multiply(v2, P))
    if (w == 0):
        print('false')
        return False
    else:
        if (w[0] % n == r):
            print('Got it!!!')
            return True
        else:
            print('EORROR!!!')
            return False

#3.Leaking k leads to leaking of d
def k_Leaking(r,n,k,s,m):
    e=hash(m)
    d=Extended_Euclidean(r,n) * (k*s-e)%n
    return d

#4.Reusing k leads to leaking of d
def k_Reuse(r1,s1,m1,r2,s2,m2,n):
    e1=hash(m1)
    e2=hash(m2)
    d=((s1 * e2 - s2 * e1) * Extended_Euclidean((s2 * r1 - s1 * r1), n)) % n
    return d

#5.Two users, using k leads to leaking of d, that is they can deduce each other’s d
def Use_the_Same_k(s1,m1,s2,m2,r,d1,d2,n):
    e1=hash(m1)
    e2=hash(m2)
    d2_1 = ((s2 * e1 - s1 * e2 + s2 * r * d1) * Extended_Euclidean(s1 * r, n)) % n
    d1_1 = ((s1 * e2 - s2 * e1 + s1 * r * d2) * Extended_Euclidean(s2 * r, n)) % n
    if(d2==d2_1 and d1_1==d1):
        print("Got it!!!")
        return 1
    else:
        print("ERROR!!!")
        return 0

#6.不验证m的验证算法
def Verify_without_m(e, n, G, r, s, P):
    w = Extended_Euclidean(s, n)
    v1 = (e * w) % n
    v2 = (r * w) % n
    w = Add(Multiply(v1, G), Multiply(v2, P))
    if (w == 0):
        print('ERROR!!!')
        return False
    else:
        if (w[0] % n == r):
            print('Got it!!!')
            return True
        else:
            print('ERROR!!!')
            return False

#7.One can forge signature if the verification does not check m
def Pretend(r, s, n, G, P):
    u = random.randrange(1, n - 1)
    v = random.randrange(1, n - 1)
    r1 = Add(Multiply(u, G), Multiply(v, P))[0]
    e1 = (r1 * u * Extended_Euclidean(v, n)) % n
    s1 = (r1 * Extended_Euclidean(v, n)) % n
    Verify_without_m(e1, n, G, r1, s1, P)

#8.Schnorr签名
def Schnorr_Sign(m, n, G, d,k):
    R = Multiply(k, G)
    e = hash(str(R[0]) + m)
    s = (k + e * d) % n
    return R, s

#9.Same d and k with ECDSA and Schnorr signature, leads to leaking of d
def Schnorr_and_ECDSA(r1, s1, R, s2, m, n):
    e1 = int(hash(m))
    e2 = int(hash(str(R[0]) + m))
    d = ((s1 * s2 - e1) * Extended_Euclidean((s1 * e2 + r1), n)) % n
    return d


#0.初始化
a = 2
b = 2
p = 17
m = 'high'
m_1="grade"
G = [5, 1]
n = 19
k=2
d = 5
P = Multiply(d, G)#公钥

#1.测试签名和验证
print("1.测试ECDSA签名和验证算法")
r,s=ECDSA_Sign(m,n,G,d,k)
print("签名为:",r,s)
print("验证结果为：")
ECDSA_Verify(m,n,G,r,s,P)
print('\n')

#2.Leaking k leads to leaking of d
print("任务二、Leaking k leads to leaking of d")
if (d == k_Leaking(r,n,k,s,m)):
    print("Got it!!!")
print("\n")

#3.Reusing k leads to leaking of d
print("任务三、Reusing k leads to leaking of d")
r_1,s_1=ECDSA_Sign(m_1,n,G,d,k)
r_2,s_2=ECDSA_Sign(m,n,G,7,k)
if (d == k_Reuse(r,s,m,r_1,s_1,m_1,n)):
    print("Got it!!!")
print('\n')

#4.Two users, using k leads to leaking of d, that is they can deduce each other’s d
print("任务四、Two users, using k leads to leaking of d, that is they can deduce each other’s d")
print("验证结果为：")
Use_the_Same_k(s_1,m_1,s_2,m,r,5,7,n)
print('\n')

#5.Malleability, e.g. (r,s) and (r,-s) are both valid signatures, lead to blockchain network split
print("任务五、Malleability, e.g. (r,s) and (r,-s) are both valid signatures, lead to blockchain network split")
print("测试结果为：")
ECDSA_Verify(m,n,G,r,-s,P)
print('\n')

#6.One can forge signature if the verification does not check m
print("任务六、One can forge signature if the verification does not check m")
print("伪装是否成功：")
Pretend(r,s,n,G,P)
print('\n')

#7.Same d and k with ECDSA and Schnorr signature, leads to leaking of d
print("任务七、Same d and k with ECDSA and Schnorr signature, leads to leaking of d")
r3,s3=Schnorr_Sign(m,n,G,d,k)#第六问
d2=Schnorr_and_ECDSA(r,s,r3,s3,m,n)
print("破解是否成功：")
print(d == d2)
print('\n')


