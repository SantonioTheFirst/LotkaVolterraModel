import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy import integrate
from time import time
import seaborn as sns


sns.set_style('darkgrid')

a = 1.
b = 1.
c = 1.
k = 1.
dt = 0.0001
tmax = 20
t = int(tmax / dt)
t_range = np.arange(0, tmax, dt)
y = 3


def Volterra(x, y, a, b, c, k):
    '''
    dx/dt = -ax + bxy
    dy/dt = cy - kxy

    dx/x = (by - a)dt
    dy/y = (c - kx)dt

    lnx = (by - a)t + C
    lny = (c - kx)t + C

    lnx = byt - at + C
    lny = ct - kxt + C

    x = e^(t(by - a) + C)
    y = e^(t(c - kx) + C)

    x = Ce^(t(by - a))
    y = Ce^(t(c - kx))

    t == 0
    x0 = C
    y0 = C
    '''
    x0, y0 = x, y
    x = [x0]
    y = [y0]
    
    for i in range(t - 1):
        xnew = x[i - 1] + (-a * x[i - 1] + b * x[i - 1] * y[i - 1]) * dt
        ynew = y[i - 1] + (c * y[i - 1] - k * x[i - 1] * y[i - 1]) * dt
        x.append(xnew)
        y.append(ynew)

    return x, y


def plot(result):
    fig, (ax1, ax2) = plt.subplots(figsize=(16, 9), nrows=1, ncols=2)
    ax1.plot(t_range, result[0], label='Хищник')
    ax1.plot(t_range, result[1], label='Жертва')

    ax1.legend(loc='best')
    ax1.set_xlabel('Время')
    ax1.set_ylabel('Популяция')

    ax2.plot(result[0], result[1])
    ax2.set_xlabel('Популяция хищников')
    ax2.set_ylabel('Популяция жертв')
    plt.grid(True)
    plt.show()


def reset(event):
    alpha.reset()
    beta.reset()
    gamma.reset()
    delta.reset()


def update(val):
    a = alpha.val
    b = beta.val
    c = gamma.val
    k = delta.val
    for i, x in enumerate(X):
        result = Volterra(x, y, a, b, c, k)
        plots[i].set_xdata(result[0])
        plots[i].set_ydata(result[1])
        

X = [1, 2, 3]
plots = []

fig = plt.plot(figsize=(16, 9))
for x in X:
    result = Volterra(x, y, a, b, c, k)
    p, = plt.plot(result[0], result[1], label=f'x={x}, y={y}')
    plots.append(p)
plt.subplots_adjust(left=0.1, bottom=0.3)
plt.title('Модель "хищник-жертва"') #+ fr'$\alpha={a}, \beta={b}, \gamma={c}, \delta={k}$')
plt.xlabel('Популяция хищников')
plt.ylabel('Популяция жертв')
plt.legend(loc='upper right')
plt.grid(True)

axes_alpha = plt.axes([0.1, 0.20, 0.8, 0.02])
axes_beta = plt.axes([0.1, 0.15, 0.8, 0.02])
axes_gamma = plt.axes([0.1, 0.1, 0.8, 0.02])
axes_delta = plt.axes([0.1, 0.05, 0.8, 0.02])
alpha = Slider(ax=axes_alpha, label=r'$\alpha$', valmin=0.0, valmax=5.0, valinit=1.0)
beta = Slider(ax=axes_beta, label=r'$\beta$', valmin=0.0, valmax=5.0, valinit=1.0)
gamma = Slider(ax=axes_gamma, label=r'$\gamma$', valmin=0.0, valmax=5.0, valinit=1.0)
delta = Slider(ax=axes_delta, label=r'$\delta$', valmin=0.0, valmax=5.0, valinit=1.0)

resetax = plt.axes([0.8, 0.015, 0.1, 0.04])
button = Button(resetax, 'Сброс', color='gold', hovercolor='skyblue')

alpha.on_changed(update)
beta.on_changed(update)
gamma.on_changed(update)
delta.on_changed(update)

button.on_clicked(reset)

plt.show()
