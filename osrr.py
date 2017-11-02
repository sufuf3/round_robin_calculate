# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


def genarate_linechart(turnaround):
    print(turnaround)
    plt.plot(turnaround.keys(), turnaround.values(), 'ro', linestyle='-')
    plt.axis([1, len(turnaround) + 1, 0, max(turnaround.values()) + 2])
    plt.show()


def avg_time(around_time, psnum):
    total_num = 0
    for i in around_time:
        total_num = total_num + i
    avgtime = total_num / psnum
    return avgtime


def turnaround_time(psaroundtime_list, list_lenth, psnum):
    around_time = [0]
    all_around_time = []
    all_lenth = list_lenth
    tmp_list = []
    total_time = 0
    while list_lenth > 0:
        listlen = len(psaroundtime_list)
        for i in range(0, listlen):
            tmp = None
            try:
                tmp = psaroundtime_list[i].pop()
                list_lenth = list_lenth - 1
                if len(psaroundtime_list[i]) == 0:
                    all_around_time.append(
                        around_time[all_lenth - list_lenth - 1] + tmp)
            except BaseException:
                if tmp_list.count(i) == 0:
                    tmp_list.append(i)
            if tmp is not None and len(tmp_list) != len(psaroundtime_list) - 1:
                try:
                    around_time.append(
                        around_time[all_lenth - list_lenth - 1] + tmp)
                except BaseException:
                    continue
                total_time = total_time + tmp
            elif tmp is not None:
                total_time = total_time + tmp
    # print(all_around_time)
    return all_around_time


def psaround_time(processes, quantum):
    caculate_array = []
    list_lenth = 0
    for i in range(1, len(processes) + 1):
        ca_list = []
        runtime1 = int(processes[i]) / quantum
        runtime2 = int(processes[i]) % quantum
        if runtime2 != 0:
            list_lenth = list_lenth + 1
            ca_list.append(runtime2)
        for i in range(1, int(runtime1) + 1):
            ca_list.append(quantum)
            list_lenth = list_lenth + 1
        caculate_array.append(ca_list)
    return caculate_array, list_lenth


def set_processes():
    all_ps = {}
    print("Please enter total processes(This is a integer): ")
    pnum = input()
    try:
        if int(pnum):
            for p in range(1, int(pnum) + 1):
                print(
                    "Please set the process time(This is a integer) of P" +
                    str(p) +
                    "(process 1): ")
                pt = input()
                all_ps[p] = pt
        return all_ps
    except BaseException:
        set_processes()


def set_maxquantum():
    print("Please set the max time quantum(This is a integer): ")
    maxq = input()
    try:
        if int(maxq):
            return int(maxq)
    except BaseException:
        set_maxquantum()


def set_guess():
    print("Please set the guess time(This is a integer): ")
    g = input()
    try:
        if int(g):
            return int(g)
    except BaseException:
        set_guess()


def set_burst():
    print("Please set the array number(This is a integer): ")
    n = input()
    burst_list = []
    for i in range(0, int(n)):
        print("Please set the CPU burst time" +
              str(i + 1) + "(This is a integer): ")
        b = input()
        burst_list.append(int(b))
    return burst_list


def predict_chart(guess_list, burst_list):
    print(guess_list)
    print(burst_list)
    ind = np.arange(len(guess_list))  # the x locations for the groups
    width = 0.35       # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, tuple(guess_list), width, color='b')
    rects2 = ax.bar(ind + width, tuple(burst_list), width, color='g')
    ax.set_ylabel('τi & ti')
    ax.set_title('Prediction of the Length of the Next CPU Burst')
    ax.set_xticks(ind + width / 2)

    ax.legend((rects1[0], rects2[0]), ('guess(i)', 'CPU burst time'))
    plt.show()


def next_bursttime(guess, burst):
    # τn+1=0.5τn+(0.5-1)Tn
    guess_list = [guess]
    for i in range(0, len(burst)):
        next_guess = float(guess_list[i]) * 0.5 + float(burst[i]) * 0.5
        guess_list.append(next_guess)
    return guess_list


def continue_run():
    print("Would you want to run another question(Y/N): ")
    run_con = input()
    if run_con == "Y" or run_con == "y" or run_con == "yes" or \
       run_con == "Yes" or run_con == "YES":
        main()
    elif run_con == "N" or run_con == "n" or run_con == "no" or \
            run_con == "No" or run_con == "NO":
        print("Bye Bye! OS TA is a nice guy! ♥ ♥ ♥ ")


def main():
    """ Choose the question """
    print("Please choose the question you'd like to run:\n\
          1) Produce the curve with P1=6, P2=3, P3=1, P4=7 and time quantum=1~7.\n\
          2) Produce the curve with P1~n = T1~n and time quantum=1~m.\n\
          3) Genearte the curve to predict the length of the next CPU burst.\n\
          4) Genearte the curve to predict the length of the next CPU burst with input parameers.\n\
          The number you'd like to choise is: ")
    qnum = input()
    # try:
    if int(qnum) < 1 or int(qnum) > 4:
        main()
    else:
        if int(qnum) == 1:
            turnaroundtime_set = {}
            processes = {1: "6", 2: "3", 3: "1", 4: "7"}
            for qt in range(1, 8):
                psaroundtime, list_lenth = psaround_time(processes, qt)
                avgaroundtime = turnaround_time(
                    psaroundtime, list_lenth, len(processes))
                turnaroundtime_set[qt] = avg_time(
                    avgaroundtime, len(processes))
            genarate_linechart(turnaroundtime_set)
            continue_run()
        elif int(qnum) == 2:
            """ Input process number, every process time. And input max time quantum.
            Then generate the data and display the curve. """
            turnaroundtime_set = {}
            processes = set_processes()
            max_quantum = set_maxquantum()
            for qt in range(1, max_quantum + 1):
                psaroundtime, list_lenth = psaround_time(processes, qt)
                avgaroundtime = turnaround_time(
                    psaroundtime, list_lenth, len(processes))
                turnaroundtime_set[qt] = avg_time(
                    avgaroundtime, len(processes))
            genarate_linechart(turnaroundtime_set)
            continue_run()
        elif int(qnum) == 3:
            burst_list = [6, 4, 6, 4, 13, 13, 13]
            guess_list = next_bursttime(10, burst_list)
            predict_chart(guess_list[:-1], burst_list)
            continue_run()
        elif int(qnum) == 4:
            guess = set_guess()
            burst_list = set_burst()
            guess_list = next_bursttime(guess, burst_list)
            predict_chart(guess_list[:-1], burst_list)
            continue_run()
    # except:
        # main()


if __name__ == "__main__":
    main()
