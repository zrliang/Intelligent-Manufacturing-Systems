
import numpy as np
import time
import copy


''' ================= initialization setting ======================'''
num_job=20 # number of jobs

p=[10,10,13,4,9,4,8,15,7,1,9,3,15,9,11,6,5,14,18,3]
d=[50,38,49,12,20,105,73,45,6,64,15,6,92,43,78,21,15,50,150,99]
w=[10,5,1,5,10,1,5,10,5,1,5,10,10,5,1,10,5,5,1,5]
# raw_input is used in python 2
population_size=int(input('Please input the size of population: ') or 30) # default value is 30
crossover_rate=float(input('Please input the size of Crossover Rate: ') or 0.8) # default value is 0.8
mutation_rate=float(input('Please input the size of Mutation Rate: ') or 0.1) # default value is 0.1
mutation_selection_rate=float(input('Please input the mutation selection rate: ') or 0.5)
num_mutation_jobs=round(num_job*mutation_selection_rate)
num_iteration=int(input('Please input number of iteration: ') or 150) # default value is 2000


start_time = time.time()

'''==================== main code ==============================='''
'''----- generate initial population -----'''
Tbest=999999999999999
best_list,best_obj=[],[]
population_list=[]
for i in range(population_size): #母體數10
    random_num=list(np.random.permutation(num_job)) # generate a random permutation of 0 to num_job-1
    population_list.append(random_num) # add to the population_list

#print(population_list)

T_best_list=[]
for n in range(num_iteration):
    Tbest_now=99999999999           
    '''-------- crossover --------'''
    parent_list=copy.deepcopy(population_list)
    offspring_list=copy.deepcopy(population_list)
    S=list(np.random.permutation(population_size)) # generate a random sequence to select the parent chromosome to crossover
    #[0,2,1,3,...]

    for m in range(int(population_size/2)): #5
        crossover_prob=np.random.rand()
        if crossover_rate>=crossover_prob: #幾成會交配
            parent_1= population_list[S[2*m]][:]
            parent_2= population_list[S[2*m+1]][:]
            child_1=['na' for i in range(num_job)]
            child_2=['na' for i in range(num_job)]

            #隨機選擇方式，將基因數一半的位置設為固定不變
            fix_num=round(num_job/2) #進位
            g_fix=list(np.random.choice(num_job, fix_num, replace=False)) #num_job中挑fix_num個亂數
            for g in range(fix_num):
                child_1[g_fix[g]]=parent_2[g_fix[g]]
                child_2[g_fix[g]]=parent_1[g_fix[g]]
            #挑出剩下一半的值
            c1=[parent_1[i] for i in range(num_job) if parent_1[i] not in child_1]
            c2=[parent_2[i] for i in range(num_job) if parent_2[i] not in child_2]
            
            #將'na'換掉
            for i in range(num_job-fix_num):
                child_1[child_1.index('na')]=c1[i]
                child_2[child_2.index('na')]=c2[i]
            offspring_list[S[2*m]]=child_1[:]
            offspring_list[S[2*m+1]]=child_2[:]
        
    '''--------mutatuon--------'''   
    for m in range(len(offspring_list)): #10
        mutation_prob=np.random.rand()
        if mutation_rate >= mutation_prob: #突變率(幾條突變)
            m_chg=list(np.random.choice(num_job, num_mutation_jobs, replace=False)) #幾個點要突變 chooses the position to mutation
            t_value_last=offspring_list[m][m_chg[0]] # save the value which is on the first mutation position
            for i in range(num_mutation_jobs-1): #-1
                offspring_list[m][m_chg[i]]=offspring_list[m][m_chg[i+1]] # displacement
            
            offspring_list[m][m_chg[num_mutation_jobs-1]]=t_value_last # move the value of the first mutation position to the last mutation position
    
    
    '''--------fitness value(calculate tardiness)-------------'''
    total_chromosome=copy.deepcopy(parent_list)+copy.deepcopy(offspring_list) # parent and offspring chromosomes combination
    chrom_fitness,chrom_fit=[],[]
    total_fitness=0
    for i in range(population_size*2):
        ptime=0
        tardiness=0
        for j in range(num_job):
            ptime=ptime+p[total_chromosome[i][j]]
            tardiness=tardiness+w[total_chromosome[i][j]]*max(ptime-d[total_chromosome[i][j]],0)
        chrom_fitness.append(1/tardiness)
        chrom_fit.append(tardiness)
        total_fitness=total_fitness+chrom_fitness[i] #一代的總延遲
    
    '''----------selection----------'''
    pk,qk=[],[]
    
    for i in range(population_size*2):
        pk.append(chrom_fitness[i]/total_fitness)
    for i in range(population_size*2):
        cumulative=0
        for j in range(0,i+1):
            cumulative=cumulative+pk[j]
        qk.append(cumulative)
    
    selection_rand=[np.random.rand() for i in range(population_size)]
    
    for i in range(population_size):
        if selection_rand[i]<=qk[0]:
            population_list[i]=copy.deepcopy(total_chromosome[0]) #只等於他?
        else:
            for j in range(0,population_size*2-1):
                if selection_rand[i]>qk[j] and selection_rand[i]<=qk[j+1]:
                    population_list[i]=copy.deepcopy(total_chromosome[j+1])
                    break


    '''----------comparison----------'''
    for i in range(population_size*2):
        if chrom_fit[i]<Tbest_now:
            Tbest_now=chrom_fit[i]
            sequence_now=copy.deepcopy(total_chromosome[i])
    
    if Tbest_now<=Tbest:
        Tbest=Tbest_now
        sequence_best=copy.deepcopy(sequence_now)
    
    T_best_list.append(Tbest)

    job_sequence_ptime=0
    num_tardy=0
    for k in range(num_job):
        job_sequence_ptime=job_sequence_ptime+p[sequence_best[k]]
        if job_sequence_ptime>d[sequence_best[k]]:
            num_tardy=num_tardy+1

'''----------result----------'''
print("optimal value: ",Tbest)
print("optimal sequence: ",sequence_best)
print("average tardiness: ",Tbest/num_job)
print("number of tardy jobs: ",num_tardy)
print('runnung_time: ',time.time() - start_time)


import matplotlib.pyplot as plt

plt.plot([i for i in range(len(T_best_list))],T_best_list,'b') #x,y為list資料
plt.ylabel('total weighted tardiness',fontsize=15)
plt.xlabel('generation',fontsize=15)
plt.show()

#'''--------plot gantt chart-------'''
#import pandas as pd
#import plotly.plotly as py
#import plotly.figure_factory as ff
#import plotly.offline as offline
#import datetime
#
#j_keys=[j for j in range(num_job)]
#j_count={key:0 for key in j_keys}
#m_count=0
#j_record={}
#for i in sequence_best:
#   gen_t=int(p[i])
#   j_count[i]=j_count[i]+gen_t
#   m_count=m_count+gen_t
#   
#   if m_count<j_count[i]:
#       m_count=j_count[i]
#   elif m_count>j_count[i]:
#       j_count[i]=m_count
#   start_time=str(datetime.timedelta(seconds=j_count[i]-p[i])) # convert seconds to hours, minutes and seconds
#
#   end_time=str(datetime.timedelta(seconds=j_count[i]))
#   j_record[i]=[start_time,end_time]
#       
#
#df=[]
#for j in j_keys:
#   df.append(dict(Task='Machine', Start='2018-07-14 %s'%(str(j_record[j][0])), Finish='2018-07-14 %s'%(str(j_record[j][1])),Resource='Job %s'%(j+1)))
#
## colors={}
## for i in j_keys:
##     colors['Job %s'%(i+1)]='rgb(%s,%s,%s)'%(255/(i+1)+0*i,5+12*i,50+10*i)
#
#fig = ff.create_gantt(df, colors=['#008B00','#FF8C00','#E3CF57','#0000CD','#7AC5CD','#ED9121','#76EE00','#6495ED','#008B8B','#A9A9A9','#A2CD5A','#9A32CD','#8FBC8F','#EEC900','#EEE685','#CDC1C5','#9AC0CD','#EEA2AD','#00FA9A','#CDB38B'], index_col='Resource', show_colorbar=True, group_tasks=True, showgrid_x=True)
#py.iplot(fig, filename='GA_flow_shop_scheduling_tardyjob', world_readable=True)