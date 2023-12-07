import matplotlib.pyplot as plt
import numpy as np

def display_graph(expr):
    x = np.linspace(-10, 10, 400)
    y = eval(expr)

    plt.figure(figsize=(8, 6))
    plt.plot(x, y)

    plt.title("Graph of " + expr)
    plt.xlabel("x")
    plt.ylabel("y")

    plt.grid()
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

    plt.show()