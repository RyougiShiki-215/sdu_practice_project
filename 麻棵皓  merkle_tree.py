import hashlib
import time

def hash_fun_node(a,b):    #用来对非叶子节点进行哈希
    mes_hash=hashlib.new("sha256")
    mes_hash.update((str(0x01)+a+b).encode())
    hash_=mes_hash.hexdigest()
    return hash_

def hash_fun_leaf(x):    #用来对叶子节点进行哈希
    mes_hash=hashlib.new("sha256")
    mes_hash.update((str(0x00)+x).encode())
    hash_=mes_hash.hexdigest()
    return hash_

class node:
    def __init__(self,s):
        self.value=s
        self.parent=None
        self.child_l=None
        self.child_r=None
        self.brother=None
        self.flag=0   #用来标记底下是否有挂载记录,0代表无挂载，1代表有挂载
        self.item=None   #用来存底下挂载的记录


'''              
def find_node(t,target):   #寻找某一节点
    f=None
    if t.flag==1:
        if t.item==target:
            return t
    if t.child_l!=None:
        f=find_node(t.child_l,target)
        if f!=None:
            return f
    if t.child_r!=None:
        f=find_node(t.child_r,target)
        if f!=None:
            return f
    return None
'''

class tree:
    def __init__(self):
        self.num=0
        self.root=None
        self.node_list=list()
    
    def create(self,lis):   #创建一个merkle tree
        
        self.num=len(lis)
        while len(lis)>1:
            n1=lis.pop(0)
            a=n1.value
            n2=lis.pop(0)
            b=n2.value
            if self.num%2==0:
                if len(lis)>self.num/2:
                    a_hash=hash_fun_leaf(a)
                    b_hash=hash_fun_leaf(b)
                    n1.item=n1.value
                    n2.item=n2.value
                    n1.value=a_hash
                    n2.value=b_hash
                    #n1=node(a_hash)
                    #n2=node(b_hash)
                    n1.flag=1
                    n2.flag=1

                else:
                    a_hash=a
                    b_hash=b

            else:
                if len(lis)>self.num/2+1:
                    a_hash=hash_fun_leaf(a)
                    b_hash=hash_fun_leaf(b)
                    n1.item=n1.value
                    n2.item=n2.value
                    n1.value=a_hash
                    n2.value=b_hash
                    #n1=node(a_hash)
                    #n2=node(b_hash)
                    n1.flag=1
                    n2.flag=1
                if len(lis)==self.num/2+1:
                    a_hash=hash_fun_leaf(a)
                    n1.item=n1.value
                    n1.value=a_hash
                    b_hash=b
                    n1.flag=1

                if len(lis)<self.num/2+1:
                    a_hash=a
                    b_hash=b


            hash_=hash_fun_node(a_hash,b_hash)           
            n3=node(hash_)            
            n3.child_l=a
            n3.child_r=b
            n1.parent=n3
            n2.parent=n3
            n1.brother=n2
            n2.brother=n1
            lis.append(n3)
            self.node_list.append(n1)
            self.node_list.append(n2)
            #self.node_list.append(n3)
        self.root=n3
    
    def search(self,target):
        for i in range(self.num):
            if (int(self.node_list[i].item)<=int(target))&(int(self.node_list[i+1].item)>=int(target)):
                return i


    def find_node(self,target):
        for i in range(self.num):
            t=self.node_list[i]
            if t.flag==1:
                if t.item==target:
                    return t    
    
    def inclusion(self,target_):   #某一个节点t的存在性证明
        time_begin=time.time()  
        t=self.find_node(target_)
        #print(t.value)
           
        while hash_fun_node(t.value,t.brother.value)!=self.root.value:
            if t.parent!=None:
                t=t.parent
            else:
                time_en=time.time()
                print('用时:',time_en-time_begin,'s')
                return 0

        time_en=time.time()
        print('用时:',time_en-time_begin,'s')
        return 1                

    def exclusion(self,target_):
        i=self.search(target_)
        if (int(self.node_list[i+1].item)>int(target_))&(int(self.node_list[i].item)<int(target_)):
            print(target_,'不在merkle tree中')


           
#if __name__ == '__main__':

#以下为任务1
#Construct a Merkle tree with 10w leaf nodes:
print('------------------------任务1---------------------')
mer_li=list()
for i in range(100000):
    mer_li.append(node(str(2*i)))

print('------------接下来开始创建merkle tree---------------')
time_start=time.time()
mer=tree()
mer.create(mer_li)
time_end=time.time()
print('创建成功！')
print('根节点哈希值为:',mer.root.value)
print('共用时:',time_end-time_start,'s')

#以下为任务2
#Build inclusion proof for specified element:
print('------------------------任务2---------------------')

item_test=str(1002)    #测试数据
print('接下来证明',item_test,'在merkle tree中')
flag=mer.inclusion(item_test)
if flag==1:
    print(item_test,'在merkle tree中')
else:
    print(item_test,'不在merkle tree中')

#以下为任务3
#Build exclusion proof for specified element
print('----------------------任务3---------------------')
item_test_2=str(3001)
print('接下来证明',item_test_2,'不在merkle tree中')
t1=time.time()
mer.exclusion(item_test_2)
t2=time.time()
print("用时：",t2-t1,'s')