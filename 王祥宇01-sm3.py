def CycleLeft(x,k):
    x='{:032b}'.format(x)
    k=k%32
    x=x[k:]+x[:k]
    return int(x,2)

def grouping(m):
    n=len(m)//128
    b=[]
    for i in range(n):
        b.append(m[i*128:(i+1)*128])
    return b


#4.常数与函数
#4.1初始值
iv='7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'


#4.2常数
def T(j):
    if j<16:
        return 0x79cc4519
    return 0x7a879d8a

#4.3布尔函数
def FF(x,y,z,j):
    if j<16:
        return x^y^z
    return (x&y)|(y&z)|(z&x)
def GG(x,y,z,j):
    if j<16:
        return x^y^z
    return (x&y)|(~x&z)

#4.4置换函数
def P0(x):
    return x^CycleLeft(x, 9)^CycleLeft(x, 17)
def P1(x):
    return x^CycleLeft(x, 15)^CycleLeft(x, 23)


#5.算法描述
#5.1概述：明文m长度小于64bit，消息填充->迭代压缩，杂凑值为256bit

#5.2填充
def fill(m):#均以十六进制为单位
    a=len(m)*4
    m=m+'8'
    k=112-(len(m)%128)
    m=m+'0'*k+'{:016x}'.format(a)
    return m


#5.3迭代压缩
#5.3.2消息扩展
def extend(x):
    w=[]
    for i in range(16):
        w.append(int(x[i*8:(i+1)*8],16))
    for j in range(16,68):
        w.append(P1(w[j-16]^w[j-9]^\
                    CycleLeft(w[j-3], 15))^CycleLeft(w[j-13], 7)^w[j-6])
    for j in range(68,132):
        w.append(w[j-68]^w[j-64])
    return w

#5.3.3压缩函数CF
def CF(vi,bi):
    w=extend(bi)
    a,b,c,d,e,f,g,h=int(vi[0:8],16),\
                     int(vi[8:16],16),\
                     int(vi[16:24],16),int(vi[24:32],16),\
                     int(vi[32:40],16),int(vi[40:48],16),\
                     int(vi[48:56],16),int(vi[56:64],16)
    for j in range(64):
        ss1=CycleLeft((CycleLeft(a,12)+e+CycleLeft(T(j),j))%pow(2,32),7)
        ss2=ss1^CycleLeft(a,12)
        tt1=(FF(a,b,c,j)+d+ss2+w[j+68])%pow(2,32)
        tt2=(GG(e,f,g,j)+h+ss1+w[j])%pow(2,32)
        d=c
        c=CycleLeft(b,9)
        b=a
        a=tt1
        h=g
        g=CycleLeft(f,19)
        f=e
        e=P0(tt2)
    abcdefgh=int('{:08x}'.format(a)+\
                 '{:08x}'.format(b)+'{:08x}'\
                 .format(c)+'{:08x}'.format(d)\
                 +'{:08x}'.format(e)+'{:08x}'.\
                 format(f)+'{:08x}'.format(g)+\
                 '{:08x}'.format(h),16)
    return '{:064x}'.format(abcdefgh^int(vi,16))

#5.3.1迭代过程
def iteration(b):
    n=len(b)
    v=iv
    for i in range(n):
        v=CF(v,b[i])
    return v

#5.4杂凑值
def sm3hash(m):#m为16进制串
    m=fill(m)
    b=grouping(m)
    return iteration(b)

#print(sm3hash(hex(5)))
