import sys
import itertools
import functools
import copy

input = open(0).read().strip()

def to_int(binary_str):
    return int(binary_str,2)

class Snail:
    def __init__(self, snail_raw, child_type, parent):
        self.parent=parent
        self.child_type=child_type
        if snail_raw.isnumeric():
            self.value=int(snail_raw)
            self.type="literal"
            return
        self.type="compound"
        lb_count=0
        rb_count=0
        i_start=0
        i=i_start
        for c in list(snail_raw):
            if c == '[':
                lb_count+=1
            if c == ']':
                rb_count+=1
            if c == ',' and  lb_count<=rb_count+1:
                left_snail_raw=''.join(list(snail_raw)[i_start+1:i])
                self.left=Snail(left_snail_raw, "left", self)
                #print(left_snail_raw)
                right_snail_raw=''.join(list(snail_raw)[i+1:-1])
                self.right=Snail(right_snail_raw,"right",self)
                #print(right_snail_raw)

            i+=1

        self.children = []

    def print_snail(self):
        if self.type=='literal':
            return str(self.value)
        else:
            return "["+self.left.print_snail()+","+self.right.print_snail()+"]"

    def add_snail(self,other_snail):
        s=Snail("","",None)
        s.type="compound"
        s.left=self
        s.left.parent=s
        s.left.child_type="left"
        s.right=other_snail
        s.right.parent=s
        s.right.child_type="right"
        return s

    def is_explode_cand(self):
        if (self.parent is not None) and (self.parent.parent is not None) and (self.parent.parent.parent is not None) and  (self.parent.parent.parent.parent is not None) and self.type != "literal" and self.right.type=="literal" and self.left.type=="literal":
            return True
        return False

    def find_explode_cand(self):
        if self.is_explode_cand():
            return self
        elif self.type!="compound":
            return None
        else:
            left_search=self.left.find_explode_cand()
            if left_search is not None:
                return left_search
            return self.right.find_explode_cand()

    def find_split_cand(self):
        if self.type=="literal" and self.value>9:
            return self
        elif self.type=="literal":
            return None
        else:
            left_search=self.left.find_split_cand()
            if left_search is not None:
                return left_search
            return self.right.find_split_cand()

    def reduce(self):
        do_search=True
        while do_search:
            do_search=False
            explode_cand=self.find_explode_cand()
            if explode_cand is not None:
 #               print(f'exploding {explode_cand.type}')
  #              print(f'exploding {explode_cand.print_snail()}')
                explode_cand.explode()
                do_search=True
                continue
            split_cand=self.find_split_cand()
            if split_cand is not None:
                split_cand.split()
                do_search=True


    def split(self):
#        print(f"split {self.print_snail()}") 
        self.type="compound"
        self.left=Snail("","left",self)
        self.left.type="literal"
        self.left.value=self.value//2
        self.right=Snail("","right",self)
        self.right.type="literal"
        self.right.value=self.value//2+self.value%2

    def explode(self):
        left_update=self.find_nearest_left()
        if left_update is not None:
            left_update.value+=self.left.value
        right_update=self.find_nearest_right()
        if right_update is not None:
            right_update.value+=self.right.value
        
        self.type="literal"
        self.value=0

    def find_nearest_left(self):
        if self.child_type=="right":
            node=self.parent.left
            while node.type != "literal":
                node=node.right
            return node
        elif self.child_type=="left":
            node=self.parent
            while node.child_type=="left":
                node=node.parent
            if node.child_type=="":
                return None
            node=node.parent.left
            while node.type != "literal":
                node=node.right
            return node

    def find_nearest_right(self):
        if self.child_type=="left":
            node=self.parent.right
            while node.type != "literal":
                node=node.left
            return node
        elif self.child_type=="right":
            node=self.parent
            while node.child_type=="right":
                node=node.parent
            if node.child_type=="":
                return None
            node=node.parent.right
            while node.type != "literal":
                node=node.left
            return node

    def get_score(self):
        if self.type=='literal':
            return self.value
        else:
            return 3*self.left.get_score()+2*self.right.get_score()



snails_raw=input.split('\n')
#print(snails_raw)
snails=[]
for snail_raw in snails_raw:
    snails.append(Snail(snail_raw,"",None))

res_snail=None
#for snail in snails:
#    if res_snail is not None:
#        res_snail=res_snail.add_snail(snail)
#        res_snail.reduce()
#    else:
#        res_snail=snail
#    #print(snail.print_snail())
#    #print(snail.reduce())
#print(res_snail.print_snail())
#print(res_snail.get_score())

for xm,ym in list(itertools.product(snails, snails)):
    x=copy.deepcopy(xm)
    y=copy.deepcopy(ym)
    res_snail=x.add_snail(y)
    res_snail.reduce()
    print(res_snail.get_score())
