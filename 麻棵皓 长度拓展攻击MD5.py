# -*- codeding = uft-8 -*-

#以下到197行为止为摘自网络的md5加密算法

def int2bin(n, count=24):
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

class MD5(object):
    # 初始化密文
    def __init__(self, message,flag=0,iv=None):
        self.message = message
        self.ciphertext = ""

        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476
        self.init_A = 0x67452301
        self.init_B = 0xEFCDAB89
        self.init_C = 0x98BADCFE
        self.init_D = 0x10325476
        '''
        self.A = 0x01234567
        self.B = 0x89ABCDEF
        self.C = 0xFEDCBA98
        self.D = 0x76543210
         '''

        if flag==1:
            self.change_iv(iv)


        #设置常数表T
        self.T = [0xD76AA478,0xE8C7B756,0x242070DB,0xC1BDCEEE,0xF57C0FAF,0x4787C62A,0xA8304613,0xFD469501,
                    0x698098D8,0x8B44F7AF,0xFFFF5BB1,0x895CD7BE,0x6B901122,0xFD987193,0xA679438E,0x49B40821,
                    0xF61E2562,0xC040B340,0x265E5A51,0xE9B6C7AA,0xD62F105D,0x02441453,0xD8A1E681,0xE7D3FBC8,
                    0x21E1CDE6,0xC33707D6,0xF4D50D87,0x455A14ED,0xA9E3E905,0xFCEFA3F8,0x676F02D9,0x8D2A4C8A,
                    0xFFFA3942,0x8771F681,0x6D9D6122,0xFDE5380C,0xA4BEEA44,0x4BDECFA9,0xF6BB4B60,0xBEBFBC70,
                    0x289B7EC6,0xEAA127FA,0xD4EF3085,0x04881D05,0xD9D4D039,0xE6DB99E5,0x1FA27CF8,0xC4AC5665,
                    0xF4292244,0x432AFF97,0xAB9423A7,0xFC93A039,0x655B59C3,0x8F0CCC92,0xFFEFF47D,0x85845DD1,
                    0x6FA87E4F,0xFE2CE6E0,0xA3014314,0x4E0811A1,0xF7537E82,0xBD3AF235,0x2AD7D2BB,0xEB86D391]
        #循环左移位数
        self.s = [7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
                    5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
                    4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
                    6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21]
        self.m = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
                    1,6,11,0,5,10,15,4,9,14,3,8,13,2,7,12,
                    5,8,11,14,1,4,7,10,13,0,3,6,9,12,15,2,
                    0,7,14,5,12,3,10,1,8,15,6,13,4,11,2,9]



    # 附加填充位
    def fill_text(self):
        for i in range(len(self.message)):
            c = int2bin(ord(self.message[i]), 8)
            self.ciphertext += c

        if (len(self.ciphertext)%512 != 448):
            if ((len(self.ciphertext)+1)%512 != 448):
                self.ciphertext += '1'
            while (len(self.ciphertext)%512 != 448):
                self.ciphertext += '0'

        length = len(self.message)*8
        if (length <= 255):
            length = int2bin(length, 8)
        else:
            length = int2bin(length, 16)
            temp = length[8:12]+length[12:16]+length[0:4]+length[4:8]
            length = temp

        self.ciphertext += length
        while (len(self.ciphertext)%512 != 0):
            self.ciphertext += '0'
        

    # 分组处理（迭代压缩）
    def circuit_shift(self, x, amount):
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    def change_pos(self):
        a = self.A
        b = self.B
        c = self.C
        d = self.D
        self.A = d
        self.B = a
        self.C = b
        self.D = c

    def FF(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.F(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp)%pow(2, 32)
        self.change_pos()

    def GG(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.G(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp)%pow(2, 32)
        self.change_pos()

    def HH(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.H(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp)%pow(2, 32)
        self.change_pos()

    def II(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.I(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp)%pow(2, 32)
        self.change_pos()


    def F(self, X, Y, Z):
        return (X & Y) | ((~X) & Z)
    def G(self, X, Y, Z):
        return (X & Z) | (Y & (~Z))
    def H(self, X, Y, Z):
        return X ^ Y ^ Z
    def I(self, X, Y, Z):
        return Y ^ (X | (~Z))

    def group_processing(self):
        M = []
        for i in range(0, 512, 32):
            num = ""
            # 获取每一段的标准十六进制形式
            for j in range(0, len(self.ciphertext[i:i+32]), 4):
                temp = self.ciphertext[i:i+32][j:j + 4]
                temp = hex(int(temp, 2))
                num += temp[2]
            # 对十六进制进行小端排序
            num_tmp = ""
            for j in range(8, 0, -2):
                temp = num[j-2:j]
                num_tmp += temp

            num = ""
            for i in range(len(num_tmp)):
                num += int2bin(int(num_tmp[i], 16), 4)
            M.append(num)

        #print(M)



        for j in range(0, 16, 4):
            self.FF(M[self.m[j]], self.s[j], self.T[j])
            self.FF(M[self.m[j+1]], self.s[j+1], self.T[j+1])
            self.FF(M[self.m[j+2]], self.s[j+2], self.T[j+2])
            self.FF(M[self.m[j+3]], self.s[j+3], self.T[j+3])

        for j in range(0, 16, 4):
            self.GG(M[self.m[16+j]], self.s[16+j], self.T[16+j])
            self.GG(M[self.m[16+j+1]], self.s[16+j+1], self.T[16+j+1])
            self.GG(M[self.m[16+j+2]], self.s[16+j+2], self.T[16+j+2])
            self.GG(M[self.m[16+j+3]], self.s[16+j+3], self.T[16+j+3])


        for j in range(0, 16, 4):
            self.HH(M[self.m[32+j]], self.s[32+j], self.T[32+j])
            self.HH(M[self.m[32+j+1]], self.s[32+j+1], self.T[32+j+1])
            self.HH(M[self.m[32+j+2]], self.s[32+j+2], self.T[32+j+2])
            self.HH(M[self.m[32+j+3]], self.s[32+j+3], self.T[32+j+3])


        for j in range(0, 16, 4):
            self.II(M[self.m[48+j]], self.s[48+j], self.T[48+j])
            self.II(M[self.m[48+j+1]], self.s[48+j+1], self.T[48+j+1])
            self.II(M[self.m[48+j+2]], self.s[48+j+2], self.T[48+j+2])
            self.II(M[self.m[48+j+3]], self.s[48+j+3], self.T[48+j+3])

        self.A = (self.A+self.init_A)%pow(2, 32)
        self.B = (self.B+self.init_B)%pow(2, 32)
        self.C = (self.C+self.init_C)%pow(2, 32)
        self.D = (self.D+self.init_D)%pow(2, 32)
        '''
        print("A:{}".format(hex(self.A)))
        print("B:{}".format(hex(self.B)))
        print("C:{}".format(hex(self.C)))
        print("D:{}".format(hex(self.D)))
        '''
        answer = ""
        for register in [self.A, self.B, self.C, self.D]:
            register = hex(register)[2:]
            for i in range(8, 0, -2):
                answer += str(register[i-2:i])

        return answer
    

    #以下为长度拓展攻击的代码

    def change_iv(self,iv):
        A=list('12345678')
        B=list('12345678')
        C=list('12345678')
        D=list('12345678')
        A[0:2]=iv[6:8]
        A[2:4]=iv[4:6]
        A[4:6]=iv[2:4]
        A[6:8]=iv[0:2]
        B[0:2]=iv[14:16]
        B[2:4]=iv[12:14]
        B[4:6]=iv[10:12]
        B[6:8]=iv[8:10]
        C[0:2]=iv[22:24]
        C[2:4]=iv[20:22]
        C[4:6]=iv[18:20]
        C[6:8]=iv[16:18]
        D[0:2]=iv[30:32]
        D[2:4]=iv[28:30]
        D[4:6]=iv[26:28]
        D[6:8]=iv[24:26]
        A=''.join(A)
        B=''.join(B)
        C=''.join(C)
        D=''.join(D)
        self.A=int(A,base=16)
        self.B=int(B,base=16)
        self.C=int(C,base=16)
        self.D=int(D,base=16)
        self.init_A = self.A
        self.init_B = self.B
        self.init_C = self.C
        self.init_D = self.D
    
    def add_mes(self,append):
        self.ciphertext=self.ciphertext+bin(int(append,base=16))[2:]


def length_attack(message,append):
    mes_out = MD5(message)
    mes_out.fill_text()
    mes_md5 = mes_out.group_processing()
    pad=get_pad(message)
    #md5_in=zhenghe(message,pad,append)
    md5_out=MD5(message)
    md5_out.fill_text()
    md5_out.add_mes(append)
    md5_out.fill_text()
    final=MD5(append,1,mes_md5)
    final.ciphertext=md5_out.ciphertext[-512:]
    #print(final.ciphertext)
    final_md5=md5_out.group_processing()
    #print(len(final_md5))
    return final_md5

def zhenghe(message,pad,append):
    final=bin(int(message,base=16))[2:]+bin(int(pad,base=16))[2:]+bin(int(append,base=16))[2:]
    #print(len(pad))
    final_re=hex(int(final,base=2))[2:]
    return final_re


def get_pad(message):   
    mes=bin(int(message,base=16)).replace('0b','')
    length=len(mes)
    pad=mes+'1'
    l=length+1
    while l%512!=448:
        pad=pad+'0'
        l+=1
    add_len=bin(length)[2:]
    
    if len(add_len)>=64:
        add_len_final=add_len[-64:]
    else:
        add_len_final=add_len
        while len(add_len_final)<64:
            add_len_final=add_len_final+'0'
    
    pad=pad+add_len_final
    #print(len(pad))
    padding_final=pad[-(len(pad)-length):]
    return hex(int(padding_final,base=2))[2:]


def length_attack_verify(message,append):
    pad=get_pad(message)
    #print(pad)
    #print(len(message)+len(pad))
    md5_in=zhenghe(message,pad,append)
    md5_out=MD5(message)
    md5_out.fill_text()
    md5_out.add_mes(append)
    md5_out.fill_text()
    #print(md5_out.ciphertext)
    result = md5_out.group_processing()
    return result


message = 'f357'
append='f47'
md5_attack=length_attack(message,append)
md5_ver=length_attack_verify(message,append)
print('message+padding+append 通过长度拓展攻击获得的md5为：',md5_attack)
print('message+padding+append 实际md5为：',md5_ver)



