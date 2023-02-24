"""
Created on Tue Jun 23 10:22:00 2022 @author: Ye Wang

Run and post-process the green heat TEA
"""

from greenheatpy.process_cost import uncertainty_cost
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import matplotlib

locations=[ 'Pilbara', 'Gladstone', 'Burnie',  'Pinjara',  'Upper Spencer Gulf']
cases=['CST',
       'CST-modular',
       'TES-HYBRID',
       'TES-PV',
       'TES-WIND',
       'BAT-HYBRID',
       'BAT-PV',
       'BAT-WIND',
       'PHES-HYBRID',
       'PHES-PV',
       'PHES-WIND'
        ]

workdir='/media/yewang/Data/Work/Research/Topics/yewang/HILTCRC/results/CF-curves-new-wind'

#for location in locations:
#    for case in cases:
        #uncertainty_cost(location, case, resdir=workdir, num_sample=10000, dev=0.25, verbose=False, plot=False)

for location in locations:

    cases=['CST', 'CST-modular', 'TES-PV', 'TES-WIND', 'TES-HYBRID','BAT-PV','BAT-WIND','BAT-HYBRID','PHES-PV','PHES-WIND','PHES-HYBRID']
    linestyles=['-', '-', '-', '-', 'o', '--', '--', '^', '-.', '-.', 's'] 

    norm = matplotlib.colors.Normalize(vmin=1, vmax=20)
    c_map=cm.tab20c
    scalar_map=cm.ScalarMappable(cmap=c_map, norm=norm)
    colors=[ scalar_map.to_rgba(5), scalar_map.to_rgba(6), scalar_map.to_rgba(9), scalar_map.to_rgba(1), scalar_map.to_rgba(13), scalar_map.to_rgba(9), scalar_map.to_rgba(1), scalar_map.to_rgba(13), scalar_map.to_rgba(9), scalar_map.to_rgba(1), scalar_map.to_rgba(13)] #

    colors_bd=[ scalar_map.to_rgba(7), scalar_map.to_rgba(8), scalar_map.to_rgba(11), scalar_map.to_rgba(3), scalar_map.to_rgba(15), scalar_map.to_rgba(11), scalar_map.to_rgba(3), scalar_map.to_rgba(15), scalar_map.to_rgba(11), scalar_map.to_rgba(3), scalar_map.to_rgba(15)]

    plot_lines = []
    fts=14
    fig, ax = plt.subplots()

    for i in range(len(cases)):
        case=cases[i]

        fn=workdir+'/post/uncertainty/LCOH_statistics_%s_%s.csv'%(case, location)
        data=np.loadtxt(fn, delimiter=',', skiprows=1)
        CF=data[:,0]
        LCOH=data[:,1]
        LCOH_min=data[:,2]
        LCOH_max=data[:,3]

        l,=ax.plot(CF, LCOH_min, linestyles[i], c=colors_bd[i])
        l,=ax.plot(CF, LCOH_max, linestyles[i], c=colors_bd[i])
        ax.fill_between(CF, LCOH_min, LCOH_max, alpha=0.1, color=colors[i])
        l,=ax.plot(CF, LCOH, linestyles[i], c=colors[i])


        plot_lines.append(l)

    ax2 = ax.twinx()
    ll=["TES", "Batt", "PHES"]
    ls=['-', '--', '-.']
    for ss, sty in enumerate(ls):
        ax2.plot(np.NaN, np.NaN, ls=ls[ss],
                 label=ll[ss], c='black')
    ax2.get_yaxis().set_visible(False)

    #legend1 = plt.legend([plot_lines[0],plot_lines[1],plot_lines[2],plot_lines[3]], ["CST", "CST-md", "PV", "Wind"], loc=1, bbox_to_anchor=(1.33,1.), fontsize=fts)
    #ax.legend([plot_lines[4],plot_lines[7], plot_lines[10]] , ["PV+Wind+TES", "PV+Wind+Batt", "PV+Wind+PHES"], loc=1, bbox_to_anchor=(1.492,0.66), fontsize=fts)
    #plt.gca().add_artist(legend1)

    #ax2.legend(loc=1, bbox_to_anchor=(1.58,1), fontsize=fts)


    ax.set_ylabel('LCOH (USD/MWh$_\mathrm{th}$)', fontsize=fts)
    ax.set_xlabel('Capacity factor (%)', fontsize=fts)
    ax.xaxis.set_tick_params(labelsize=fts)
    ax.yaxis.set_tick_params(labelsize=fts)
    ax.set_ylim([20, 60])
    #plt.title(case)
    plt.title(location)
    plt.savefig(open('%s/post/uncertainty/Comparison-LCOH-CF-%s-zoom.png'%(workdir, location),'wb'), bbox_inches='tight', dpi=300)
    #plt.show()
    plt.close()


