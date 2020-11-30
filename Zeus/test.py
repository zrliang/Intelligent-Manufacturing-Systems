import pandas as pd

walk_speed=1.2
pickup_time=20
elevator_time=30
elevator_distance=6

input1_string = input("1F 儲位: ")
list1 = input1_string.split()
list1 = list(map(int, list1))
list1.insert(0,1)
input2_string = input("2F 儲位: ")
list2 = input2_string.split()
list2 = list(map(int, list2))
list2.insert(0,91)

F_elevator_time=0
F_elevator_distance=0

df_1F = pd.read_excel("./1&2F_distance.xlsx", sheet_name=0, index_col=0)
df_2F = pd.read_excel("./1&2F_distance.xlsx", sheet_name=1, index_col=0)

total_distance=0
total_pickup_time=0
total_distance_1F=0
total_distance_2F=0
storage_1F_num=len(list1)-1
storage_2F_num=len(list2)-1

if input1_string !="1" and  input2_string !="91":
    if len(list1)>1:
        for i in range(storage_1F_num):
            total_distance_1F += df_1F.at[list1[i], list1[i+1]]

    if len(list2)>1:
        for i in range(storage_2F_num):
            total_distance_2F += df_2F.at[list2[i], list2[i+1]]
            
        F_elevator_time+=elevator_time
        F_elevator_distance+=elevator_distance

    total_distance = total_distance_1F + total_distance_2F + F_elevator_distance
    total_pickup_time= (storage_1F_num + storage_2F_num)*pickup_time + (total_distance_1F + total_distance_2F + F_elevator_distance)/walk_speed + F_elevator_time
    print("1F 儲位: ",list1[1:])
    print("2F 儲位: ",list2[1:])
    print("total_distance: ",round(total_distance,2),"m")
    print("total_pickup_time: ",round(total_pickup_time,2),"秒")
else:
    if input1_string =="1" and input2_string !="91":
        print("distance: ",df_1F.at[1, 1],"m")
        print("pickup_time: ",round(df_1F.at[1, 1]/walk_speed + pickup_time,2),"秒")
        #print()
    elif input1_string !="1" and input2_string =="91":
        print("distance: ",df_2F.at[91, 91]+ elevator_distance)
        print("pickup_time: ",round( (df_2F.at[91, 91]+elevator_distance) /walk_speed + pickup_time + elevator_time ,2),"秒")
    else:
        print("distance: ",df_1F.at[1, 1]+df_2F.at[91, 91]+ elevator_distance)
        print("pickup_time: ",round((df_1F.at[1, 1]+df_2F.at[91, 91]+elevator_distance)/walk_speed + pickup_time*2 + elevator_time ,2),"秒")