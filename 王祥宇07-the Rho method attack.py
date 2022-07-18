import sys
sys.path.append('D:\桌面')
from sm3 import sm3hash

'''
a=198
a_3=sm3hash(hex(a))
print(a_3)
print(int(str(a_3),16))
print(sm3hash(hex(int(str(a_3),16))))
'''

def repeat(x):#返回sm3hash(x)
    if isinstance(x,int):
        return sm3hash(hex(x))
    temp=int(str(x),16)
    return sm3hash(hex(temp))


import random
def Rho_method(x):#x依然得是4的倍数
    num=int(x/4)#注意python中float类型转换
    n=random.randint(0,2**(x+1)-1)
    x_a=sm3hash(hex(n))
    #temp=int(str(x_a),16)
    x_b=repeat(x_a)
    p=1
    while x_a[:num]!=x_b[:num]:
        x_a=repeat(x_a)
        x_b=repeat(repeat(x_b))
        p+=1
    print(p)
    x_b=x_a
    x_a=n
    for i in range(p):
        if repeat(x_a)[:num]==repeat(x_b)[:num]:
            return int(str(x_a),16),int(str(x_b),16)
        else:
            x_a=repeat(x_a)
            x_b=repeat(x_b)

#def verify(a):#a为元组
    


print(Rho_method(20))
#print(sm3hash(hex(31567245717694923371196878058996019188206500339240998987516367321121940145401)))
#print(sm3hash(hex(106043238390937415284607886145287880544553786701055757824032290247182571802380)))
#print(sm3hash(hex(92149844787472072187967210329932186750909454787526956128423713225310314973480)))
#print(sm3hash(hex(114815714811946478717260071032409765285919486488582428501941538422731038014732)))
#print(repeat('917d0fb47910f8ec596d47d4b7f20bde7ee77f894c5448fcb3b7ccb0b056f060'))
#print(repeat('ecb0aa4a0142321795403049501ce7fc02e44e1a96e8c058aece75ffdb68c6f8'))

    
