import matplotlib.pyplot as plt
import mpld3
import pandas as pd
import numpy as np
from config import *


import time

#plt.plot([3, 1, 4, 1, 5], 'ks-', mec='w', mew=5, ms=20)
# mpld3.show()


def graphit():
    # plt.switch_backend('Agg')
    fig = plt.figure(figsize=(10, 5))
    plt.plot([3, 1, 4, 1, 5], 'ks-', mec='w', mew=5, ms=20)
    #a = mpld3.fig_to_html(fig)
    mpld3.show()
    pass


def graph_like_distribution(line):
    plt.switch_backend('Agg')
    fig = plt.figure(figsize=(8, 4))
    line.plot(linewidth=2.5)
    plt.ylabel('likes')
    plt.xlabel('dates')
    plt.title('Like Distribution over time')
    mpld3.show()
    return mpld3.fig_to_html(fig)


def scatter_plot(xaxis, yaxis):
    # plt.switch_backend('Agg')
    fig = plt.figure(figsize=(8, 4))
    df = pd.DataFrame({'dates': xaxis, 'likes': yaxis})
    axes = df.plot('dates', 'likes',
                   kind='scatter', title='Like Distribution over time')
    mpld3.show()
    labels = list(df.columns.values)
    for i in range(len(labels)):
        tooltip = mpld3.plugins.LineLabelTooltip(
            axes.get_lines()[i], labels[i])
        mpld3.plugins.connect(plt.gcf(), tooltip)


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


#scheduler = BackgroundScheduler()
#scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
# scheduler.start()

# Shut down the scheduler when exiting the app
#atexit.register(lambda: scheduler.shutdown())
#x = np.arange(10)
#y = np.arange(10)
#line = pd.Series(data=x, index=y)
# graph_like_distribution(line)
#scatter_plot(x, y)
# graphit()
