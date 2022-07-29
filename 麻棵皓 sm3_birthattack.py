from random import randint
from time import time

iv='56b9a0600a96738016631383ab38f4914b2b917217dae4d442df30bb1e3cb0fe'

def rep(i):
    if i<16:
        return 0x79cc4519
    return 0x7a879d8a

def left_fun(x,y):
    x='{:032b}'.format(x)
    y=y%32
    x=x[y:]+x[:y]
    return int(x,2)


def bo_fun(x,y,z,a):
    if a<16:
        return x^y^z
    return (x&y)|(y&z)|(z&x)
def bo_fun2(x,y,z,a):
    if a<16:
        return x^y^z
    return (x&y)|(~x&z)


def dis0(x):
    return x^left_fun(x, 9)^left_fun(x, 17)
def dis1(x):
    return x^left_fun(x, 15)^left_fun(x, 23)


def pad(m):
    l=len(m)*4
    m=m+'8'
    k=112-(len(m)%128)
    m=m+'0'*k+'{:016x}'.format(l)
    return m

def grou(m):
    n=len(m)//128
    b=[]
    for i in range(n):
        b.append(m[i*128:(i+1)*128])
    return b

def expand(x):
    w=[]
    for i in range(16):
        w.append(int(x[i*8:(i+1)*8],16))
    for j in range(16,68):
        w.append(dis1(w[j-16]^w[j-9]^left_fun(w[j-3], 15))^left_fun(w[j-13], 7)^w[j-6])
    for j in range(68,132):
        w.append(w[j-68]^w[j-64])
    return w

def cf_rep(v,b):
    w=expand(b)
    a,b,c,d,e,f,g,h=int(v[0:8],16),int(v[8:16],16),int(v[16:24],16),int(v[24:32],16),int(v[32:40],16),int(v[40:48],16),int(v[48:56],16),int(v[56:64],16)
    for j in range(64):
        ss1=left_fun((left_fun(a,12)+e+left_fun(rep(j),j))%pow(2,32),7)
        ss2=ss1^left_fun(a,12)
        tt1=(bo_fun(a,b,c,j)+d+ss2+w[j+68])%pow(2,32)
        tt2=(bo_fun2(e,f,g,j)+h+ss1+w[j])%pow(2,32)
        d=c
        c=left_fun(b,9)
        b=a
        a=tt1
        h=g
        g=left_fun(f,19)
        f=e
        e=dis0(tt2)
    abcdefgh=int('{:08x}'.format(a)+'{:08x}'.format(b)+'{:08x}'.format(c)+'{:08x}'.format(d)+'{:08x}'.format(e)+'{:08x}'.format(f)+'{:08x}'.format(g)+'{:08x}'.format(h),16)
    return '{:064x}'.format(abcdefgh^int(v,16))

def iter(x):
    n=len(x)
    v=iv
    for i in range(n):
        v=cf_rep(v,x[i])
    return v

def sm3_(m):  #输入为16进制的字符串
    m=pad(m)
    b=grou(m)
    return iter(b)

def sm3_birth():
    sm3_list=list()
    sm3_in=list()
    for f in range(1000,1000000):
        flag=0
        x=str(hex(f))
        y=sm3_(x)
        for i in range(len(sm3_list)):
            if y[0:8]==sm3_list[i][0:8]:
                print('寻找到碰撞！')
                print('二者原相分别为：',sm3_in[i],'and',x)
                flag=1
                break
        if flag==1:
            break
        sm3_in.append(x)
        sm3_list.append(y)

t1=time()
sm3_birth()
t2=time()
print('共耗时：',t2-t1,'s')


