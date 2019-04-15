from numpy import *

def linearTrends(values,max_value):
    r=shape(values)[1]
    
    ref = arange(0,r)
    
    a=zeros(shape=(shape(values)[0],shape(values)[2]))
    
    for i in range(shape(values)[0]):
        for k in range(shape(values)[2]):
            x=values[i,::,k]
            coefficients =polyfit(x, ref, 1)
            polynomial = poly1d(coefficients)
            a[i,k]=polynomial.c[0]
            

    
    b=zeros(shape=shape(a))
    
    for j in range(shape(a)[0]):
        for n in range(shape(a)[1]):
            if a[j,n]>max_value:
                pass
            else:
                b[j,n]=n
    
    range_val=[]
    
    for g in range(shape(b)[1]):
        if (sum(b[::,g])==(shape(b)[0])*g):
            
            range_val.append(g)
        else:
            pass
            
    values=values[:,:,range_val]
    
    deleted_epochs=[]
    for m in range(shape(values)[2]):
        if m in range_val:
            pass
        else:
            deleted_epochs.append(m)
            
    
    return values,deleted_epochs
                
