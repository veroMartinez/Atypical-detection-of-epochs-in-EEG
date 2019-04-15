from numpy import *
from scipy.signal import welch

def spectral(values,max_value,Fs):
    a=zeros(shape=(shape(values)[0],(int((shape(values)[1])/2))+1,shape(values)[2]))
    epochs=shape(values)[2]
    for i in range(shape(values)[0]):
        for k in range(shape(values)[2]):
            x=values[i,::,k]

            frec,pxx=welch(x,Fs,nperseg=len(x))

            new_pxx=pxx-mean(pxx)
            

            a[i,:,k]=new_pxx


    b=zeros(shape=(shape(a)[0],shape(a)[2]))
    for j in range(shape(a)[0]):
        for n in range(shape(a)[2]):

            if any((a[:,:,n])>max_value):

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
        
    if shape(values)[2]==1:
        deleted_epochs=arange(2,epochs+1)

    return values,deleted_epochs
    
                
                
                
      
