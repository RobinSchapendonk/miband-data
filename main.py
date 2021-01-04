path = 'test/'

import datetime
from matplotlib import pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

def calculate_data(data, file_name):
    days = []
    amounts = []

    for data_points in data:
        data_points_list = data_points.split(",")
        if data_points_list[0] == "": continue

        date = data_points_list[0].split("-")
        if file_name == "sleep.csv": amount = (int(data_points_list[6]) - int(data_points_list[5])) / 60 / 60
        elif file_name == "activity.csv": amount = int(data_points_list[2])

        if amount == 0 or amount == 0.0: amounts.append(np.nan)
        else: amounts.append(amount)

        day = datetime.date(int(date[0]), int(date[1]), int(date[2])).strftime('%j')
        days.append(int(day))
    
    return [ days, amounts ]

def load (ax, file_name, ignore, ylabel):
    file = open(path + file_name, "r")
    data = file.read().split("\n")
    if ignore in data[0]: data.pop(0)
    if data[-1] == "": data = data[:-1]

    first = int(data[0].split("-")[0])
    last = int(data[-1].split("-")[0])
    diff = (last - first) + 1

    for i in range(diff):
        this_year_data = list(filter(lambda x: int(x[0:4]) == (first + i), data))
        axis = calculate_data(this_year_data, file_name)
        ax.plot(axis[0], axis[1], label=str(first + i))

    ax.set_ylabel(ylabel)
    ax.margins(0, 0)
    ax.grid(True)

fig = plt.figure()
gs = fig.add_gridspec(2, 1, hspace=0, wspace=0)
axs = gs.subplots(sharex=True)

load(axs[0], "sleep.csv", "date,lastSyncTime,deepSleepTime,shallowSleepTime,wakeTime,start,stop", "Amount of sleep (hours)")
load(axs[1], "activity.csv", "date,lastSyncTime,steps,distance,runDistance,calories", "Amount of steps")

lines, labels = fig.axes[-1].get_legend_handles_labels()
fig.legend(lines, labels, loc = 'upper center')
fig.tight_layout()

plt.xlabel("Day in the year")
plt.show()