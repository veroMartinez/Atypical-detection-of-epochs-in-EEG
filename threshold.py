from numpy import *

def threshold(values,min_value,max_value):
    x=ones(shape(values)[2])

    a=[]
   
    for i in range(shape(values)[2]):
        
        if any(values[:,:,i]>max_value):
            x[i]=0
            pass
            
               
        if any(values[:,:,i]<min_value):
            pass
        
        else:
            a.append(i)
            x[i]=0
    
    values=values[:,:,a]
    
    
   
    deleted_epochs=[]
    for m in range(shape(values)[2]):
        if m in a:
            pass
        else:
            deleted_epochs.append(m)
            
    
    return values,deleted_epochs