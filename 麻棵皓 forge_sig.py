import hashlib
import random

#以下先是ECDSA算法的代码---------
def gcd(x,y):
    while x!=0:
        x,y = y%x,x
    return y

def inv(a,p):
    while a<0:
        a=a+p
    if gcd(a,p)!=1:
        return None
    u1,u2,u3 = 1,0,a
    v1,v2,v3 = 0,1,p
    while v3!=0:
        q = u3//v3
        v1,v2,v3,u1,u2,u3 = (u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
    return u1%p


def hash_(message):

    m = hashlib.sha1()
    m.update(message)
    dig = m.hexdigest()
    hash_result = int('0x' + dig, 16)
    return hash_result

class ECDSA_point(object):

	def __init__(self, x, y):
		if x == 0 and y == 0:
			self.infinity = True
			self.point = (0, 0)
		else:
			self.infinity = False
			self.point = (x, y)

	def point(self, x, y):
		return self.point

	def x(self):
		return self.point[0]

	def y(self):
		return self.point[1]

	def isinf(self):
		return self.infinity

	def __str__(self):
		if self.isinf():
			return '(0, 0)'

		return '(%.3f, %.3f)' % (self.x(), self.y())

	def __eq__(self, o):
		if self.isinf():
			return o.isinf()

		return self.x() == o.x() and self.y() == o.y()


class ECurve(object):

	def __init__(self, a, b, p):
		# Basic conditions for the curve to be valid.
		assert a < p and b > 0 and b < p and p > 2
		assert (4 * (a ** 3) + 27 * (b ** 2))  % p != 0

		self.a = a
		self.b = b
		self.p = p
		self.zero = ECDSA_point(0, 0)

	def valid_verify(self, point):
		if point == self.zero:
			return True

		l = (point.y() ** 2) % self.p
		r = ((point.x() ** 3) + self.a * point.x() + self.b) % self.p
		return l == r

	def add(self, p1, p2):

		if p1 == self.zero:
			return p2

		if p2 == self.zero:
			return p1

		if p1.x() == p2.x() and (p1.y() != p2.y() or p1.y() == 0):
			return self.zero

		if p1.x() == p2.x():
			m = ((3 * (p1.x() ** 2)) + self.a) * inv(2 * p1.y(), self.p) % self.p
		else:
			m = (p1.y() - p2.y()) * inv(p1.x() - p2.x(), self.p) % self.p

		xR = (m ** 2 - p1.x() - p2.x()) % self.p
		yR = (m * (p1.x() - xR) - p1.y()) % self.p

		return ECDSA_point(xR, yR)

	def mul(self, p1, n):

		res = self.zero
		acc = p1
		exp = n

		while exp > 0:
			if exp % 2 != 0:
				res = self.add(res, acc)

			acc = self.add(acc, acc)
			exp //= 2

		return res


class ECDSA(object):

    def __init__(self, curve, G, n):

        self.curve_ = curve
        self._G = G
        self._n = n
        self.hash_=None


    def getkey(self):

        d = random.randint(1, self._n - 1)
        P = self.curve_.mul(self._G, d)
        return (d, P)

    def Sign(self, key, message):

        d = key[0]
        e = hash_(message)
        self.hash_=e
        r = 0
        s = 0

        while True:
            k = random.randint(1, self._n - 1)
            R_ = self.curve_.mul(self._G, k)

            r = R_.x() % self._n
            # Try again with another random k
            if r == 0:
                continue

            k1 = inv(k, self._n)

            s = (((e + r*d) % self._n) * k1) % self._n
            
            if s == 0:
                continue
            break
        return (r, s)

    def Verify(self, sig_, key):

        Q = key[1]

        if not self.curve_.valid_verify(Q):
            print(str(Q),'is wrong')

        r, s = sig_
        if r < 1 or r > self._n - 1 or s < 1 or s > self._n - 1:
            print('({},{})'.format(r,s),'越界了')

        h = self.hash_
        w = inv(s, self._n)
        u1 = (h * w) % self._n
        u2 = (r * w) % self._n
        P = self.curve_.add(self.curve_.mul(self._G, u1), self.curve_.mul(Q, u2))

        return r == (P.x() % self._n)

M = 233970423115425145524320034830162017933
G = ECDSA_point(182, 85518893674295321206118380980485522083)
N = 29246302889428143187362802287225875743

curve = ECurve(-95051, 11279326, M)
dsa = ECDSA(curve, G, N)

key = dsa.getkey()   #生成公私钥
d=key[0]
P=key[1]
print('Satoshi持有的私钥为：',d)
#接下来私钥持有人先对自己的信息进行签名并公开
sig = dsa.Sign(key, b'sdu hello')
print('Satoshi对 sdu hello 的签名为：',sig)
print('对Satoshi的签名进行验证---------------------------------')
if dsa.Verify(sig, key):
    print('验证通过！')
else:
    print('验证不通过！')

print('\n')

#--------签名伪造-------------------
print('-----接下来对Satoshi签名进行伪造，以下过程均不知道Satoshi的私钥d--------------')
u=3
v=5
R_forge=curve.add(curve.mul(G,u),curve.mul(P,v))
r_forge=R_forge.point[0]%N
e_forge=(r_forge*u*inv(v,N))%N
s_forge=(r_forge*inv(v,N))%N
dsa.hash_=e_forge
print('伪造签名信息的哈希为:',e_forge)
print('伪造的签名为：',(r_forge,s_forge))


#---------对伪造签名进行验证---------------------
print('接下来对伪造签名进行验证----------------------------------')
if dsa.Verify((r_forge,s_forge), key):
    print('验证通过！')
else:
    print('验证不通过！')



