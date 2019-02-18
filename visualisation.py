import matplotlib.dates as mdates
import numpy as np
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def stacked_bar_area_times(instances, areas):

    employee_data = []
    plots = []

    for x, instance in enumerate(instances):

        values = [h.total_seconds()/60.0 for h in instance.area_times.values()]
        employee_data.append({'name': instance.employee,
                              'values': values})
        if x == 0:
            plots.append(plt.bar(range(len(instance.area_times)), values, 0.35))
        else:
            plots.append(plt.bar(range(len(instance.area_times)), values, 0.35, bottom=employee_data[x-1]['values']))

    area_names = []
    for area in areas:
        area_names.append(area.area_name)

    employee_names = []
    for employee in employee_data:
        employee_names.append(employee['name'])

    legend_data = []
    for plot in plots:
        legend_data.append(plot[0])

    plt.ylabel('Time (minutes)')
    plt.title('Time by Area and Employee')
    plt.xticks(range(len(areas)), tuple(area_names))
    plt.yticks(np.arange(0, 301, 50))
    plt.legend(tuple(legend_data), tuple(employee_names))
    plt.savefig('./graphs/area_within.png')


def stacked_bar_area_times_near(instances, areas):

    employee_data = []
    plots = []

    for x, instance in enumerate(instances):

        values = [h.total_seconds()/60.0 for h in instance.near_area_times.values()]
        employee_data.append({'name': instance.employee,
                              'values': values})
        if x == 0:
            plots.append(plt.bar(range(len(instance.near_area_times)), values, 0.35))
        else:
            plots.append(plt.bar(range(len(instance.near_area_times)), values, 0.35, bottom=employee_data[x-1]['values']))

    area_names = []
    for area in areas:
        area_names.append(area.area_name)

    employee_names = []
    for employee in employee_data:
        employee_names.append(employee['name'])

    legend_data = []
    for plot in plots:
        legend_data.append(plot[0])

    plt.ylabel('Time (minutes)')
    plt.title('Time by Area and Employee')
    plt.xticks(range(len(areas)), tuple(area_names))
    plt.yticks(np.arange(0, 301, 50))
    plt.legend(tuple(legend_data), tuple(employee_names))
    plt.savefig('./graphs/area_near.png')


def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d})".format(pct, absolute)


def pie_most_visited_area(instances, areas):

    area_names = []
    for area in areas:
        area_names.append(area.area_name)

    sizes = [0 for area in area_names]
    for instance in instances:
        sizes = [x + y for x, y in zip(sizes, instance.area_visits.values())]

    for x, value in enumerate(sizes):
        if value == 0:
            del area_names[x]
            del sizes[x]

    fig1, ax1 = plt.subplots()
    ax1.set_title("Areas most visited")
    ax1.pie(sizes, labels=area_names, autopct=lambda pct: func(pct, sizes), startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('./graphs/area_visits.png')


def line_speed(instances):
    for instance in instances:
        if instance.speed is not None:
            fig, ax = plt.subplots()
            ax.plot(instance.df['time'].loc[1:], instance.speed)

            plt.ylabel('Speed (degrees per second)')
            plt.xlabel('Time')
            plt.title('Speed vs Time for ' + instance.employee)
            ax.grid()
            plt.gcf().subplots_adjust(left=0.2, bottom=0.1)

            plt.savefig("./graphs/speed_" + instance.employee.replace(' ', '_') + ".png")
