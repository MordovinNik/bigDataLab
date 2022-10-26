from statistics import median

import matplotlib
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, time, date
import matplotlib.dates as mdates
from hurst import compute_Hc, random_walk

matplotlib.use('TkAgg')

def slideMedian(sample, m):
    res = []
    for i in range(sample.size):
        # check for edge cases
        if i < m:
            res.append(np.median(sample[0: 2 * i + 1]))
        elif i >= sample.size - m - 1:
            res.append(np.median(sample[i - (sample.size - i): sample.size]))
        # default case
        else:
            res.append(np.median(sample[i - m: i + m + 1]))
    return res


def prony(x: np.array, T: float):
    if len(x) % 2 == 1:
        x = x[:len(x) - 1]

    p = len(x) // 2

    shift_x = [0] + list(x)
    a = sp.linalg.solve([shift_x[p + i:i:-1] for i in range(p)], -x[p::])

    z = np.roots([*a[::-1], 1])

    h = sp.linalg.solve([z ** n for n in range(1, p + 1)], x[:p])

    f = 1 / (2 * np.pi * T) * np.arctan(np.imag(z) / np.real(z))
    alfa = 1 / T * np.log(np.abs(z))
    A = np.abs(h)
    fi = np.arctan(np.imag(h) / np.real(h))

    return f, alfa, A, fi


def kandell(x, x_m):
    r = np.array(x) - np.array(x_m)
    r_e = 2.0 / 3.0 * (len(x) - 2)
    r_d = (16 * len(x) - 29) / 90.0
    k_c, p_val = sp.stats.kendalltau(x_m, r)
    print("tau = ", k_c)
    rp_count = np.array(
        [1 if (r[i + 1] > r[i] and r[i + 1] > r[i + 2]) or (r[i + 1] < r[i] and r[i + 1] < r[i + 2]) else 0 for i in
         range(r.size - 2)]).sum()
    print("RP count:", rp_count)
    print("E:", r_e)
    print("D:", r_d)
    if r_e + r_d > rp_count > r_e - r_d:
        print('Случайный')
    elif rp_count < r_e - r_d:
        print('Значения коррелированы')
    elif rp_count > r_e + r_d:
        print('Быстро колеблется')


if __name__ == '__main__':
    h = 0.02
    x = []
    for i in range(1, 201):
        s = 0
        for k in range(1, 4):
            s += k * np.exp(-h * i / k) * np.cos(4 * np.pi * k * h * i + np.pi / k)
        x.append(s)

    f, alpha, A, fi = prony(np.array(x), 0.1)
    plt.stem(2 * A)
    plt.grid()

    # 2

    data = pd.read_csv("data.csv")

    data["Average"] = data["Average"].astype(float)
    data["Date"] = [datetime.strptime(str(d), '%Y%m%d') for d in data['Date']]
    print(data["Date"])
    data = data.loc[:, ['Date', 'Average']]

    trend = slideMedian(np.array(data["Average"]), 55)
    trend2 = slideMedian(np.array(data["Average"]), 1500)

    plt.show()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.plot(data["Date"], data['Average'], label='temp')

    plt.plot(data["Date"], trend, label="trend")
    plt.plot(data["Date"], trend2, label="trend_1500")
    plt.grid()
    plt.legend()

    kandell(data["Average"], trend)
    kandell(data["Average"], trend2)

    H, c, data = compute_Hc(trend, kind='random_walk', simplified=False)

    f, ax = plt.subplots()
    ax.plot(data[0], c * data[0] ** H, color="deepskyblue")
    ax.scatter(data[0], data[1], color="purple")
    print(H)
    
    plt.show()
