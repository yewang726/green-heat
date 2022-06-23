
import numpy as np
import os
import matplotlib.pyplot as plt

results=np.array([])

RM=np.append(np.arange(1, 5, 0.5), np.arange(5, 11, 2))
SH=np.arange(0., 20, 1)

m=int(len(RM))
n=int(len(SH))

location='Newman'
casedir='./results/%s'%location
for rm in RM:
    for sh in SH:

        res_fn=casedir+'/summary_%.1f_%.1f.csv'%(rm, sh)
        data=np.loadtxt(res_fn, dtype=str, delimiter=',')
        results=np.append(results, data[:,1].astype(float))

results=results.reshape(int(len(results)/9), 9)


RM=results[:,0].reshape(m,n)
SH=results[:,1].reshape(m,n)
CF=results[:,2].reshape(m,n)
R=results[:,4].reshape(m,n)
BT_Cap=results[:,7].reshape(m,n)
BT_P=results[:,8].reshape(m,n)


for i in range(m):
    plt.plot(SH[i], CF[i], label='RM = %s'%RM[i,0])

#plt.xlim([0,2.5])
plt.xlabel('Storage hour')
plt.ylabel('CF')
plt.legend(loc=1, bbox_to_anchor=(1.3,1.))
plt.savefig(open(casedir+'/CF.png', 'wb'),  bbox_inches='tight')
#plt.show()
plt.close()

for i in range(m):
    plt.plot(SH[i], R[i], label='RM = %s'%RM[i,0])

#plt.xlim([0,2.5])
plt.xlabel('Storage hour')
plt.ylabel('PV ratio')
plt.legend(loc=1, bbox_to_anchor=(1.3,1.))
plt.savefig(open(casedir+'/r_pv.png', 'wb'),  bbox_inches='tight')
#plt.show()
plt.close()





