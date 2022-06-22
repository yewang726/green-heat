
import numpy as np
import os
import matplotlib.pyplot as plt

results=np.array([])
t_storage=np.append(np.arange(0., 3.2, 0.2), np.arange(4, 20, 2))


location='Newman'
casedir='./results/%s'%location
for RM in range(1, 10):
    for SH in t_storage:

        res_fn=casedir+'/summary_%.1f_%.1f.csv'%(RM, SH)
        data=np.loadtxt(res_fn, dtype=str, delimiter=',')
        results=np.append(results, data[:,1].astype(float))

results=results.reshape(int(len(results)/9), 9)


RM=results[:,0].reshape(9,24)
SH=results[:,1].reshape(9,24)
CF=results[:,2].reshape(9,24)
R=results[:,4].reshape(9,24)
BT_Cap=results[:,7].reshape(9,24)
BT_P=results[:,8].reshape(9,24)

check=BT_Cap/BT_P
print(check)

for i in range(9):
    plt.plot(SH[i], CF[i], label='RM = %s'%RM[i,0])

plt.xlim([0,2.5])
plt.xlabel('Storage hour')
plt.ylabel('CF')
plt.legend(loc=1, bbox_to_anchor=(1.3,1.))
plt.savefig(open(casedir+'/CF.png', 'wb'),  bbox_inches='tight')
#plt.show()
plt.close()

for i in range(9):
    plt.plot(SH[i], R[i], label='RM = %s'%RM[i,0])

plt.xlim([0,2.5])
plt.xlabel('Storage hour')
plt.ylabel('PV ratio')
plt.legend(loc=1, bbox_to_anchor=(1.3,1.))
plt.savefig(open(casedir+'/r_pv.png', 'wb'),  bbox_inches='tight')
#plt.show()
plt.close()


for i in range(9):
    plt.plot(SH[i], BT_Cap[i], label='RM = %s'%RM[i,0])

plt.xlim([0,2.5])
plt.xlabel('Storage hour')
plt.ylabel('Battery capacity (MWh)')
plt.legend(loc=1, bbox_to_anchor=(1.3,1.))
plt.savefig(open(casedir+'/battery_capacity.png', 'wb'),  bbox_inches='tight')
#plt.show()
plt.close()


for i in range(9):
    plt.plot(SH[i], BT_P[i], label='RM = %s'%RM[i,0])

plt.xlim([0,2.5])
plt.xlabel('Storage hour')
plt.ylabel('Battery power (MW)')
plt.legend(loc=1, bbox_to_anchor=(1.3,1.))
plt.savefig(open(casedir+'/battery_power.png', 'wb'),  bbox_inches='tight')
#plt.show()
plt.close()




