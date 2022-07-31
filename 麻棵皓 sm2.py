from random import randint
import math

#由于sm2需要用到sm3，以下先复制之前的sm3代码

iv='56b9a0600a96738016631383ab38f4914b2b917217dae4d442df30bb1e3cb0fe'   #sm3算法的iv变量

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

def inv(xx,p):
    x1,x2,x3=1,0,xx
    y1,y2,y3=0,1,p
    while y3!=0:
        q=x3//y3
        t1,t2,t3=x1-q*y1,x2-q*y2,x3-q*y3
        x1,x2,x3=y1,y2,y3
        y1,y2,y3=t1,t2,t3
    return x1%p

def add_(x1,y1,x2,y2,xx,p):
    if x1==x2 and y1==p-y2:
        return False
    if x1!=x2:
        lamda=((y2-y1)*inv(x2-x1, p))%p
    else:
        lamda=(((3*x1*x1+xx)%p)*inv(2*y1, p))%p
    x3=(lamda*lamda-x1-x2)%p
    y3=(lamda*(x1-x3)-y1)%p
    return x3,y3

def point(x,y,g,xx,p):
    g=bin(g)[2:]
    qx,qy=x,y
    for i in range(1,len(g)):
        qx,qy=add_(qx, qy, qx, qy, xx, p)
        if g[i]=='1':
            qx,qy=add_(qx, qy, x, y, xx, p)
    return qx,qy

def kdf(f,glen):
    ct=1
    k=''
    for _ in range(math.ceil(glen/256)):
        k=k+sm3_(hex(int(f+'{:032b}'.format(ct),2))[2:])
        ct=ct+1
    k='0'*((256-(len(bin(int(k,16))[2:])%256))%256)+bin(int(k,16))[2:]
    return k[:glen]


gx=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
gy=0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7


dB=randint(1,n-1)
xB,yB=point(gx,gy,dB,a,p)


def encrypt(m:str):
    plen=len(hex(p)[2:])
    m='0'*((4-(len(bin(int(m.encode().hex(),16))[2:])%4))%4)+bin(int(m.encode().hex(),16))[2:]
    klen=len(m)
    while True:
        k=randint(1, n)
        while k==dB:
            k=randint(1, n)
        x2,y2=point(xB, yB, k, a, p)
        x2,y2='{:0256b}'.format(x2),'{:0256b}'.format(y2)
        t=kdf(x2+y2, klen)
        if int(t,2)!=0:
            break
    x1,y1=point(gx, gy, k, a, p)
    x1,y1=(plen-len(hex(x1)[2:]))*'0'+hex(x1)[2:],(plen-len(hex(y1)[2:]))*'0'+hex(y1)[2:]
    c1='04'+x1+y1
    c2=((klen//4)-len(hex(int(m,2)^int(t,2))[2:]))*'0'+hex(int(m,2)^int(t,2))[2:]
    c3=sm3_(hex(int(x2+m+y2,2))[2:])
    return c1,c2,c3

def decrypt(c1,c2,c3,a,b,p):
    c1=c1[2:]
    x1,y1=int(c1[:len(c1)//2],16),int(c1[len(c1)//2:],16)
    if pow(y1,2,p)!=(pow(x1,3,p)+a*x1+b)%p:
        return False
    x2,y2=point(x1, y1, dB, a, p)
    x2,y2='{:0256b}'.format(x2),'{:0256b}'.format(y2)
    klen=len(c2)*4
    t=kdf(x2+y2, klen)
    if int(t,2)==0:
        return False
    m='0'*(klen-len(bin(int(c2,16)^int(t,2))[2:]))+bin(int(c2,16)^int(t,2))[2:]
    u=sm3_(hex(int(x2+m+y2,2))[2:])
    if u!=c3:
        return False
    mes=hex(int(m,2))[2:]
    mes=str(bytes.fromhex(mes))
    mes='\n'.join(mes[2:-1].split('\\n'))
    return mes

def sign(m:str):
    sig=encrypt(m)
    return sig

def verify(sig,a,b,p,m):
    mes=decrypt(sig[0],sig[1],sig[2],a,b,p)
    if m==mes:
        print('验证通过！')
    else:
        print('验证不通过！')

message='hellosdu'
print('要加密的明文为：')
print(message)
m1,m2,m3=encrypt(message)
m=(m1+m2+m3).upper()
print('加密后的密文为:')
for i in range(len(m)):
    print(m[i*8:(i+1)*8],end=' ')

print('\n解密后的明文为：')
plan=decrypt(m1, m2, m3, a, b, p)
print(plan)
print('\n')

sig_mes='sdu10422'
sig=sign(sig_mes)
print(sig_mes,'的签名为：',sig)
print('接下来验证签名---------------------------------------------------------------------')
verify(sig,a,b,p,sig_mes)

