
import numpy as np
import os
import matplotlib.pyplot as plt

results=np.array([])

RM=np.append(np.arange(1, 5, 0.5), np.arange(5, 11, 2))
SH=np.arange(1e-6, 20.+1e-6, 2.)

m=int(len(RM))
n=int(len(SH))

location='Newman'
model_name='pv_wind_TES_heat'
casedir='./results/CF-%s/%s/'%(model_name, location)
for rm in RM:
    for sh in SH:

        res_fn=casedir+'/summary_%.1f_%.1f.csv'%(rm, sh)
        
        data=np.loadtxt(res_fn, dtype=str, delimiter=',')
        results=np.append(results, data[:,1].astype(float))

results=results.reshape(int(len(results)/11), 11)


RM=results[:,0].reshape(m,n)
SH=results[:,1].reshape(m,n)
LCOH=results[:,2].reshape(m,n)
CF=results[:,3].reshape(m,n)
#R=results[:,4].reshape(m,n)
#BT_Cap=results[:,7].reshape(m,n)
#BT_P=results[:,8].reshape(m,n)


for i in range(m):
    plt.plot(SH[i], CF[i], label='RM = %s'%RM[i,0])

plt.ylim([0,1])
plt.xlabel('Storage hour')
plt.ylabel('CF')
plt.legend(loc=1, bbox_to_anchor=(1.3,1.))
plt.savefig(open(casedir+'/CF.png', 'wb'),  bbox_inches='tight')
#plt.show()
plt.close()

for i in range(m):
    plt.plot(SH[i], LCOH[i], label='RM = %s'%RM[i,0])

#plt.ylim([0,1])
plt.xlabel('Storage hour')
plt.ylabel('LCOH')
plt.legend(loc=1, bbox_to_anchor=(1.3,1.))
plt.savefig(open(casedir+'/LCOH.png', 'wb'),  bbox_inches='tight')
#plt.show()
plt.close()



'''
for i in range(m):
    plt.plot(SH[i], R[i], label='RM = %s'%RM[i,0])

#plt.xlim([0,2.5])
plt.xlabel('Storage hour')
plt.ylabel('PV ratio')
plt.legend(loc=1, bbox_to_anchor=(1.3,1.))
plt.savefig(open(casedir+'/r_pv.png', 'wb'),  bbox_inches='tight')
#plt.show()
plt.close()

'''



