# Simulate SEIRV model

Time = 359  # time
popul = 1000000  # total population
rep = 50  # number of times to repeat simulation
#repeat simulation 'rep' number of times and store outcome
datavector = []
for i in range(rep):          
    simu = simfxn(Time,popul)
    datavector.append(simu)

# plot results from simulations
plt.figure(figsize=(10.5, 5))

plt.plot([x/popul for x in simout[0]], label='S',color = '#1f77b4')
plt.plot([x/popul for x in simout[1]], label='E',color = 'yellow')
plt.plot([x/popul for x in simout[2]], label='I',color = '#d62728')
plt.plot([x/popul for x in simout[3]], label='R',color = '#2ca02c')
plt.plot([x/popul for x in simout[4]], label='V',color = '#ff7f0e')
plt.legend(loc='right')

i_each = []

for n in datavector:
    sList = [x / popul for x in n[0]]
    eList = [x / popul for x in n[1]]
    iList = [x / popul for x in n[2]]
    rList = [x / popul for x in n[3]]
    vList = [x / popul for x in n[4]]
     
    plt.plot(sList,color = '#1f77b4')
    plt.plot(eList,color = 'yellow')
    plt.plot(iList,color = '#d62728')
    plt.plot(rList,color = '#2ca02c')
    plt.plot(vList,color = '#ff7f0e')
       
    i_each.append(iList)
     
plt.tick_params(axis = 'both', which = 'major', labelsize = 20)
plt.ylabel('Population', fontsize=30) 
plt.xlabel('Time(days)', fontsize=30)
plt.show()

# plt.savefig('SEIRV_plot.pdf', bbox_inches='tight')

# VIOLIN PLOTS
#extract infection values and put in a dataframe
flat_list = [item for sublist in i_each for item in sublist]  
flat_list = []
for sublist in i_each:
    for item in sublist:
        flat_list.append(item)
        
datafr = pd.DataFrame(flat_list)

# group data into months
lst = range(0,12)
itl = list(itertools.chain.from_iterable(itertools.repeat(x, 30) for x in lst))
datafr = datafr.assign(month=itl*rep) 
datafr.columns=["inf","months"]
datafr['inf'] = pd.to_numeric(datafr['inf'], errors='coerce') # convert to numeric

#find the mean value for each month
mean = datafr.groupby(['months'])['inf'].mean().reset_index()
mean_col = datafr.groupby(['months'])['inf'].mean() # d
datafr = datafr.set_index(['months']) # 
datafr['mean_col'] = mean_col
datafr = datafr.reset_index() 
 
# plot violins
plt.figure(figsize=(10, 7))
qq = sns.violinplot(x="months", y="inf", color="skyblue",data=datafr,scale='count', bw=0.25,cut=0, inner=None)
# sns.stripplot(x="months", y="inf", data=datafr, jitter=True)
sns.swarmplot(x="months", y="inf", data=mean, color='white',edgecolor="black",linewidth=0.5, size=5)
sns.pointplot(x="months", y="inf", data=mean, color='grey',scale=0.5)
qq.set_ylabel("Infected cases (%)",fontsize=30)
qq.set_xlabel("Month",fontsize=30)
formatter = mticker.ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-2,2))
qq.yaxis.set_major_formatter(formatter)
qq.yaxis.offsetText.set_fontsize(18)
plt.setp(qq.collections, alpha=1.0)
plt.tick_params(axis = 'both', which = 'major', labelsize = 20)

plt.show()

#plt.savefig('violin_plot.pdf', bbox_inches='tight')

