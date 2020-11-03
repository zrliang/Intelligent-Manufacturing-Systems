import numpy as np

# Problem Definition and Parameters Setting
Num_Jobs = 20  
p = [10,10,13,4,9,4,8,15,7,1,9,3,15,9,11,6,5,14,18,3] 
d = [50,38,49,12,20,105,73,45,6,64,15,6,92,43,78,21,15,50,150,99]
w = [10,5,1,5,10,1,5,10,5,1,5,10,10,5,1,10,5,5,1,5]

tabusize=12
Num_Iteration=1000


tabulist = np.zeros((tabusize, 2)) #零矩陣
T_best_list=[]

#tabulist=[[1,2],[3,4]]
T_best = 9999999999
this_time_best=99999999
# Initialize the Solution
##x_now = randperm(Num_Jobs) 隨機亂序 1.3.2.4
x_now =np.random.permutation(Num_Jobs).tolist() #0-3
#print(x_now)
Ptime = 0
Tardiness = 0

for j in range(Num_Jobs):
    Ptime = Ptime + p[x_now[j]]
    Tardiness = Tardiness + w[x_now[j]]*max(Ptime-d[x_now[j]],0)
    #print(Ptime)
    #print(Tardiness)
T_best = Tardiness
x_best=x_now[:]
#print("初始解=",T_best)

#print("------------")


import time
start = time.process_time()

for t in range(Num_Iteration):
    #print("第",t+1,"次")
# Neighborhood Search
    for k in range(0,Num_Jobs-1):
        istabu = 0
        x_next = x_now[:]  #!!!
        x_next[k] = x_now[k+1]
        x_next[k+1] = x_now[k]
        #print(x_next)

    ## Find out whether the schedule is tabu or not
        for n in range(tabusize): 
            if (x_next[k] == tabulist[n][0] and x_next[k+1] == tabulist[n][1]):
                istabu = 1
            if (x_next[k] == tabulist[n][1] and x_next[k+1] == tabulist[n][0]):
                istabu = 1
        #print(istabu)

    ## If it is non-tabu results, the schedule is admissible. Then we can calculate its objective value
        if (istabu == 0):
            Ptime = 0
            Tardiness = 0
            for j in range(Num_Jobs):
                Ptime = Ptime + p[x_next[j]]
                Tardiness = Tardiness + w[x_next[j]]*max(Ptime-d[x_next[j]],0)
            
            if(Tardiness < this_time_best):
                this_time_best=Tardiness
                sequence = x_next[:]
                t1 = x_next[k]
                t2 = x_next[k+1]    
                                                              
            #print(Tardiness)
        
            if (Tardiness < T_best):
                T_best = Tardiness
                sequence = x_next[:]
                x_best=sequence[:]
                t1 = x_next[k]
                t2 = x_next[k+1]

    x_now=sequence[:]
    #print("本次最佳解",this_time_best)
    #print("下次的初始解",x_now)
    this_time_best=99999999

    # Update the Tabu List
    for n in range(-1,-tabusize,-1):
        tabulist[n][0] = tabulist [n-1][0]
        tabulist[n][1] = tabulist [n-1][1]

    tabulist[0][0] = t1
    tabulist[0][1] = t2

    # Update the Best Result of All Iterations
    # if (T_now_best <= Tbest):
    #     Tbest = T_now_best
    #     x_best = x_now

    #print(tabulist)
    T_best_list.append(T_best)
    #print("全域解",T_best)
    #print("全域順序",x_best)


# Calculate the Tardy Job Counts
end = time.process_time()
runnung_time=end-start

jobsequence_ptime = 0
num_tardy = 0
tardy_time=0
avg_tardy_time=0
for l in range(Num_Jobs):
    jobsequence_ptime = jobsequence_ptime + p[x_best[l]]
    if (jobsequence_ptime > d[x_best[l]]):
        tardy_time+=jobsequence_ptime - d[x_best[l]]
        num_tardy = num_tardy + 1
avg_tardy_time=tardy_time/Num_Jobs

print("tabusize: ",tabusize)
print("iteration: ",Num_Iteration)
print("optimal value: ",T_best_list[-1])
print("optimal job sequence: ",x_best)
print("average tardiness: ",avg_tardy_time)
print("number of tardy jobs: ",num_tardy)
print("runnung_time: ",runnung_time)

#print("number of tardy jobs:)
import matplotlib.pyplot as plt

plt.plot([i for i in range(len(T_best_list))],T_best_list,'b') #x,y為list資料
plt.ylabel('total weighted tardiness',fontsize=15)
plt.xlabel('generation',fontsize=15)
plt.show()
# print("------------")

