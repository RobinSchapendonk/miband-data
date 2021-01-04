path = 'test/'

import datetime
from matplotlib import pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

def calculate_sleep_data (data):
    total_deep_sleep_time = 0
    total_shallow_sleep_time = 0
    total_wake_time = 0

    days = []
    amounts = []

    for data_points in data:
        data_points_list = data_points.split(",")
        if data_points_list[0] == "": continue

        date = data_points_list[0].split("-")
        # last_sync_time = data_points_list[1]
        deep_sleep_time = data_points_list[2]
        shallow_sleep_time = data_points_list[3]
        wake_time = data_points_list[4]
        start = data_points_list[5]
        stop = data_points_list[6]

        amount = (int(stop) - int(start)) / 60 / 60
        if amount != 0.0: amounts.append(amount)
        else: amounts.append(np.nan)

        day = datetime.date(int(date[0]), int(date[1]), int(date[2])).strftime('%j')
        days.append(int(day))

        total_deep_sleep_time += int(deep_sleep_time)
        total_shallow_sleep_time += int(shallow_sleep_time)
        total_wake_time += int(wake_time)
    
    return [ days, amounts, total_deep_sleep_time, total_shallow_sleep_time, total_wake_time]

def calculate_step_data (data):
    total_steps = 0
    total_distance = 0
    total_run_distance = 0
    total_calories = 0

    days = []
    amounts = []

    for data_points in data:
        data_points_list = data_points.split(",")
        if data_points_list[0] == "": continue

        date = data_points_list[0].split("-")
        # last_sync_time = data_points_list[1]
        steps = data_points_list[2]
        distance = data_points_list[3]
        run_distance = data_points_list[4]
        calories = data_points_list[5]

        amount = int(steps)
        if amount != 0: amounts.append(amount)
        else: amounts.append(np.nan)

        day = datetime.date(int(date[0]), int(date[1]), int(date[2])).strftime('%j')
        days.append(int(day))

        total_steps += int(steps)
        total_distance += int(distance)
        total_run_distance += int(run_distance)
        total_calories += int(calories)
    
    return [ days, amounts, total_steps, total_distance, total_run_distance, total_calories ]

#sleep
file = open(path + "sleep.csv", "r")
data = file.read().split("\n")
if "date,lastSyncTime,deepSleepTime,shallowSleepTime,wakeTime,start,stop" in data[0]: data.pop(0)
if data[-1] == "": data = data[:-1]

first = int(data[0].split("-")[0])
last = int(data[-1].split("-")[0])

diff = (last - first) + 1

fig = plt.figure()
gs = fig.add_gridspec(2, 1, hspace=0, wspace=0)
axs = gs.subplots(sharex=True)


for i in range(diff):
    this_year_data = list(filter(lambda x: int(x[0:4]) == (first + i), data))
    axis = calculate_sleep_data(this_year_data)

    axs[0].plot(axis[0], axis[1], label=str(first + i))

axs[0].set_ylabel("Amount of sleep (hours)")
axs[0].margins(0,0)
axs[0].grid(True)
axs[0].legend(loc='best')


#activity
file = open(path + "activity.csv", "r")
data = file.read().split("\n")
if "date,lastSyncTime,steps,distance,runDistance,calories" in data[0]: data.pop(0)
if data[-1] == "": data = data[:-1]

first = int(data[0].split("-")[0])
last = int(data[-1].split("-")[0])

diff = (last - first) + 1

for i in range(diff):
    this_year_data = list(filter(lambda x: int(x[0:4]) == (first + i), data))
    axis = calculate_step_data(this_year_data)

    axs[1].plot(axis[0], axis[1], label=str(first + i))
     
axs[1].set_ylabel("Amount of steps")
axs[1].margins(0,0)
axs[1].grid(True)
axs[1].legend(loc='best')

plt.xlabel("Day in year")

fig.tight_layout()
plt.show()