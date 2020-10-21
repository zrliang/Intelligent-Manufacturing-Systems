import pandas as pd
import numpy as np
wip = pd.read_excel("./Single-Machine Scheduling Problem.xlsx", sheet_name=0, dtype=str)

x_now =np.random.permutation(Num_Jobs) #0-3
Ptime = 0
Tardiness = 0
A=[0,2,3,2]
for j in x_now:
    print(A[j])