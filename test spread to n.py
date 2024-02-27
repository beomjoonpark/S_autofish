def to_n(lst):
    new_lst=[]
    i=0
    while i < 8 :
        if i < 7 and lst[i]==lst[i+1]:
            if i < 6 and lst[i+1]==lst[i+2]:
                new_lst.append(lst[i]+'3')
                i=i+3
            else:
                new_lst.append(lst[i]+'2')
                i=i+2
        else:
            new_lst.append(lst[i]+'1')
            i=i+1
    return new_lst

def n_to(lst):
    new_lst=[]
    for i in range(len(lst)):
        for j in range(int(lst[i][1])):
            new_lst.append(lst[i][0])
    return new_lst
def check(q, pat, lstan, lstuse):
    for i in range(pat):
        if q==pat[i]:
            lstan.append[i]
    
            
        
def solve_quiz(pattern,quiz):
    patrev=list(reversed(pattern))
    pat1 = to_n(patrev)
    pat2 = []
    pat3 = []
    used1=[]
    used2=[]
    used3=[]
    for i in range(len(pat)):
        if quiz[0]==pat[i]
            used1.append(i)


            
a=['B','G','G','R','R','R','R','G']
a.reverse()
b= to_n(a)
print(b)
c= n_to(b)
print(c)
