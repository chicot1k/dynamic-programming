import numpy as np
print('Введитете вместимость рюкзака')
W=int(input())
print('Введитеть сколько дано предметов')
N=int(input())
masw = [] 
mass = []
A=[[0 for i in range(W+1)] for j in range(N+1)]
for i in range(N): 
    print(f'Введите вес {i+1}-го предмета')
    w=int(input())
    masw.append(w)
    print(f'Введите цену {i+1}-го предмета')
    s=int(input())
    mass.append(s)
print(masw)
print(mass)
for k in range(1,N+1):
    for s in range(1,W+1):
        if s>= masw[k-1]:
            A[k][s] = max(A[k - 1][s], A[k - 1][s - masw[k-1]] + mass[k-1])
        else:
            A[k][s] = A[k - 1][s]
print(A)
def findAns(k,s):
  if A[k][s] == 0: 
    return 
  if A[k - 1][s] == A[k][s]:
    findAns(k - 1, s)
  else:
    findAns(k - 1, s - masw[k-1])
    ans.append(k)
ans=[]
findAns(N,W)
print(ans)