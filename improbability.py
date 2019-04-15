from numpy import *
from scipy.stats import kurtosis

def kurt(values,max_value):
    
    a=zeros(shape=(shape(values)[0],shape(values)[2]))
    
    for i in range(shape(values)[0]):
        for k in range(shape(values)[2]):
            x=values[i,::,k]
            kurt_value=kurtosis(x)
            #print(kurt_value)
            a[i,k]=kurt_value
            
    b=zeros(shape=shape(a))
    
    for j in range(shape(a)[0]):
        for n in range(shape(a)[1]):
            if a[j,n]<0:
                absv=abs(a[j,n])
                if absv>max_value:
                    pass
                else:
                    b[j,n]=n
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