import sys
import itertools
import functools

input = open(0).read().strip()

def to_int(binary_str):
    return int(binary_str,2)

def to_binary_str(c):
    return {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111'
    }.get(c)

class Package:
    def __init__(self):
        self.children = []

    def read_literal(self, start_index):
        self.literal=''
        chunk_index=0
        self.end_index=start_index+(chunk_index+1)*5
        chunk=input_b_list[start_index+chunk_index*5:self.end_index]
        self.literal+=''.join(chunk[1:])
        while chunk[0]=='1':
            chunk_index+=1
            self.end_index=start_index+(chunk_index+1)*5
            chunk=input_b_list[start_index+chunk_index*5:self.end_index]
            self.literal+=''.join(chunk[1:])
    
    def read_headers(self, start_index):
        self.start_index=start_index
        self.version=''.join(input_b_list[start_index:start_index+3])
        #print(self.version)
        self.type=''.join(input_b_list[start_index+3:start_index+6])
        if self.type == '100':
            self.length_type=None
            self.end_index_header=start_index+6
        else:
            self.length_type=''.join(input_b_list[start_index+6:start_index+7])
            if self.length_type == '0':
                self.end_index_header=start_index+22
                self.length_value=''.join(input_b_list[start_index+7:start_index+22])
            else:
                self.end_index_header=start_index+18
                self.length_value=''.join(input_b_list[start_index+7:start_index+18])

    def get_version_sum(self):
        if self.type=='100':
            return to_int(self.version)
        else:
            return to_int(self.version)+functools.reduce(lambda a,b:a+b.get_version_sum(),self.children,0)
    
    def print_expr(self):
        if self.type=='100':
            return str(to_int(self.literal))+" "
        elif self.type=='000':
            res="(+ "
            for child in self.children:
                res+=child.print_expr()
            res+=")"
            return res 
        elif self.type=='001':
            res="(* "
            for child in self.children:
                res+=child.print_expr()
            res+=")"
            return res 
        elif self.type=='010':
            res="(min "
            for child in self.children:
                res+=child.print_expr()
            res+=")"
            return res 
        elif self.type=='011':
            res="(max "
            for child in self.children:
                res+=child.print_expr()
            res+=")"
            return res 
        elif self.type=='101':
            res="(greater "
            for child in self.children:
                res+=child.print_expr()
            res+=")"
            return res 
        elif self.type=='110':
            res="(less "
            for child in self.children:
                res+=child.print_expr()
            res+=")"
            return res 
        elif self.type=='111':
            res="(= "
            for child in self.children:
                res+=child.print_expr()
            res+=")"
            return res 
    
    def get_value(self):
        if self.type=='100':
            return to_int(self.literal)
        elif self.type=='000':
            return functools.reduce(lambda a,b:a+b.get_value(),self.children,0)
        elif self.type=='001':
            return functools.reduce(lambda a,b:a*b.get_value(),self.children,1)
        elif self.type=='010':
            return functools.reduce(lambda a,b:a if a<b.get_value() else b.get_value(),self.children,9999999999999999)
        elif self.type=='011':
            return functools.reduce(lambda a,b:a if a>b.get_value() else b.get_value(),self.children,-9999999999999999)
        elif self.type=='101':
            return 1 if self.children[0].get_value()>self.children[1].get_value() else 0
        elif self.type=='110':
            return 1 if self.children[0].get_value()<self.children[1].get_value() else 0
        elif self.type=='111':
            return 1 if self.children[0].get_value()==self.children[1].get_value() else 0


#print(input)
#for c in list(input):
#    print(to_binary_str(c))

input_b_list=''.join([to_binary_str(c) for c in list(input)])
#print(input_b_list)

#for idx,c in enumerate(list(binary_list)):
#    print(idx,c)

def create_package(created_packages, current_read_index):
    package=Package()
    created_packages.append(package)
    package.read_headers(current_read_index)
    #print(f'created {package.type} {package.length_type} at {current_read_index}')
    current_read_index=package.end_index_header
    if package.type=='100':
        package.read_literal(current_read_index)
        current_read_index=package.end_index
    elif package.length_type=='1':
        #print(to_int(package.length_value))
        package.children = create_packages_by_count(current_read_index,to_int(package.length_value))
        for child in package.children:
            current_read_index=max(current_read_index,child.end_index)
    elif package.length_type=='0':
        package.children = create_packages_by_size(current_read_index,to_int(package.length_value))
        current_read_index+=to_int(package.length_value)
    package.end_index=current_read_index
    return current_read_index


def create_packages_by_count(start_index,wanted_count):
    created_packages=[]
    current_read_index=start_index
    while len(created_packages)<wanted_count:
        current_read_index=create_package(created_packages, current_read_index)
    return created_packages


def create_packages_by_size(start_index,size):
    created_packages=[]
    current_read_index=start_index
    while current_read_index<start_index+size:
        current_read_index=create_package(created_packages, current_read_index)
    return created_packages

packages=create_packages_by_count(0,1)

#print(vars(packages[0]))
#print(packages[0].get_version_sum())
#print(packages[0].get_value())
print(packages[0].print_expr())

f = open("scheme_expr.scm", "w")
f.write(packages[0].print_expr()+"\n")
f.close()

